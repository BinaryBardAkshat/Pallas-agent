import email as email_lib
import email.message
import imaplib
import logging
import os
import smtplib
import threading
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, parseaddr
from typing import Any, Callable, List, Optional

from .base import BasePlatform

logger = logging.getLogger(__name__)


def _decode_header_value(raw: Any) -> str:
    """Decode an RFC-2047 encoded email header into a plain string."""
    if raw is None:
        return ""
    parts: List[str] = []
    for fragment, charset in decode_header(str(raw)):
        if isinstance(fragment, bytes):
            parts.append(fragment.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(fragment)
    return "".join(parts)


def _extract_body(msg: email.message.Message) -> str:
    """Extract plain-text body from an email.Message."""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in cd:
                payload = part.get_payload(decode=True)
                if isinstance(payload, bytes):
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
        return ""
    payload = msg.get_payload(decode=True)
    if isinstance(payload, bytes):
        charset = msg.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace")
    return str(payload or "")


class EmailPlatform(BasePlatform):
    platform_name: str = "email"

    def __init__(self, config: Optional[dict] = None, on_message: Optional[Callable] = None):
        super().__init__(on_message=on_message)
        self.smtp_host: str = os.getenv("EMAIL_HOST", "")
        self.smtp_port: int = int(os.getenv("EMAIL_PORT", "587"))
        self.user: str = os.getenv("EMAIL_USER", "")
        self.password: str = os.getenv("EMAIL_PASSWORD", "")
        self.imap_host: str = os.getenv("IMAP_HOST", self.smtp_host)
        self.poll_interval: int = int(os.getenv("EMAIL_POLL_INTERVAL", "30"))
        self._stop_event: threading.Event = threading.Event()
        self._poll_thread: threading.Thread = threading.Thread()  # placeholder

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self.start()

    def start(self) -> None:
        missing = []
        if not self.smtp_host:
            missing.append("EMAIL_HOST")
        if not self.user:
            missing.append("EMAIL_USER")
        if not self.password:
            missing.append("EMAIL_PASSWORD")
        if missing:
            logger.warning(
                "[%s] Missing configuration variables: %s",
                self.platform_name,
                ", ".join(missing),
            )
        else:
            print(
                f"[{self.platform_name}] Starting email poller for {self.user} "
                f"(poll every {self.poll_interval}s)."
            )

        self._stop_event.clear()
        poll_thread = threading.Thread(
            target=self._poll_loop, daemon=True, name="email-poll"
        )
        self._poll_thread = poll_thread
        poll_thread.start()

    def disconnect(self) -> None:
        self._stop_event.set()
        poll_thread = self._poll_thread
        if poll_thread.is_alive():
            poll_thread.join(timeout=self.poll_interval + 5)
        logger.info("[%s] Email poller stopped.", self.platform_name)
        print(f"[{self.platform_name}] Email poller stopped.")

    # ------------------------------------------------------------------
    # Send
    # ------------------------------------------------------------------

    def send(self, chat_id: Any, text: str, subject: str = "Pallas Agent Response") -> None:
        to_addr = str(chat_id)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to_addr
        msg["Message-ID"] = make_msgid(domain=self.user.split("@")[-1] if "@" in self.user else "pallas")
        msg.attach(MIMEText(text, "plain", "utf-8"))

        try:
            # Use SMTP_SSL for port 465, STARTTLS otherwise
            if self.smtp_port == 465:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=30) as server:
                    server.login(self.user, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(self.user, self.password)
                    server.send_message(msg)
            logger.info("[%s] Email sent to %s.", self.platform_name, to_addr)
        except smtplib.SMTPException as exc:
            logger.error("[%s] SMTP error sending to %s: %s", self.platform_name, to_addr, exc)
        except OSError as exc:
            logger.error(
                "[%s] Network error sending to %s: %s", self.platform_name, to_addr, exc
            )

    # ------------------------------------------------------------------
    # Poll loop (background thread)
    # ------------------------------------------------------------------

    def _poll_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._check_inbox()
            except Exception as exc:
                logger.error("[%s] Poll error: %s", self.platform_name, exc)
            self._stop_event.wait(timeout=self.poll_interval)

    def _check_inbox(self) -> None:
        imap_host = self.imap_host or self.smtp_host
        if not imap_host or not self.user or not self.password:
            logger.debug("[%s] Skipping poll — credentials not configured.", self.platform_name)
            return

        try:
            conn = imaplib.IMAP4_SSL(imap_host)
        except OSError as exc:
            logger.error("[%s] IMAP connection failed: %s", self.platform_name, exc)
            return

        try:
            conn.login(self.user, self.password)
            conn.select("INBOX")

            # Search for UNSEEN messages
            status, data = conn.search(None, "UNSEEN")
            if status != "OK":
                logger.warning("[%s] IMAP SEARCH failed: %s", self.platform_name, status)
                return

            raw_ids = data[0]
            if not raw_ids:
                return

            msg_ids: List[bytes] = raw_ids.split()
            for msg_id in msg_ids:
                self._fetch_and_dispatch(conn, msg_id)
        except imaplib.IMAP4.error as exc:
            logger.error("[%s] IMAP error: %s", self.platform_name, exc)
        finally:
            try:
                conn.logout()
            except Exception:
                pass

    def _fetch_and_dispatch(self, conn: imaplib.IMAP4_SSL, msg_id: bytes) -> None:
        status, msg_data = conn.fetch(msg_id.decode(), "(RFC822)")
        if status != "OK" or not msg_data:
            logger.warning("[%s] Failed to fetch message %s.", self.platform_name, msg_id)
            return

        for part in msg_data:
            if not isinstance(part, tuple):
                continue
            raw_email = part[1]
            if not isinstance(raw_email, bytes):
                continue

            parsed = email_lib.message_from_bytes(raw_email)

            from_header = parsed.get("From", "")
            _, sender_email = parseaddr(from_header)
            if not sender_email:
                sender_email = from_header

            body = _extract_body(parsed)
            subject = _decode_header_value(parsed.get("Subject", ""))
            message_id = parsed.get("Message-ID", "")

            logger.info(
                "[%s] Received email from %s (subject: %s, id: %s).",
                self.platform_name,
                sender_email,
                subject,
                message_id,
            )

            # Include subject in text so the handler has full context
            full_text = f"Subject: {subject}\n\n{body}".strip()
            self.handle(chat_id=sender_email, text=full_text)
            break  # Only process the first RFC822 part
