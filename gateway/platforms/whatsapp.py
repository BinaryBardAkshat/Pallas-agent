import logging
import os
from typing import Any, Callable, Optional

try:
    import httpx
except ImportError as _httpx_err:
    raise ImportError("httpx is required: pip install httpx") from _httpx_err

from .base import BasePlatform

logger = logging.getLogger(__name__)

TWILIO_MESSAGES_URL = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
CHUNK_SIZE = 4096


class WhatsAppPlatform(BasePlatform):
    platform_name: str = "whatsapp"

    def __init__(self, api_key: str = "", on_message: Optional[Callable] = None):
        super().__init__(token=api_key, on_message=on_message)
        self.api_key: str = api_key or os.getenv("WHATSAPP_API_KEY", "")
        self.account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.from_number: str = os.getenv("TWILIO_WHATSAPP_FROM", "")
        self._client: Optional["httpx.Client"] = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self.start()

    def start(self) -> None:
        missing = []
        if not self.api_key:
            missing.append("WHATSAPP_API_KEY")
        if not self.account_sid:
            missing.append("TWILIO_ACCOUNT_SID")
        if not self.from_number:
            missing.append("TWILIO_WHATSAPP_FROM")

        if missing:
            logger.warning(
                "[%s] Missing configuration variables: %s",
                self.platform_name,
                ", ".join(missing),
            )
        else:
            logger.info(
                "[%s] Twilio WhatsApp platform ready. From: %s",
                self.platform_name,
                self.from_number,
            )
            print(f"[{self.platform_name}] Connected. Twilio account SID: {self.account_sid}")

        self._client = httpx.Client(
            auth=(self.account_sid, self.api_key),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30.0,
        )

    def disconnect(self) -> None:
        client = self._client
        if client is not None:
            client.close()
        self._client = None
        logger.info("[%s] Disconnected.", self.platform_name)
        print(f"[{self.platform_name}] Disconnected.")

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------

    def send(self, chat_id: Any, text: str) -> None:
        client = self._client
        if client is None:
            logger.error(
                "[%s] send() called before connect()/start(). Call connect() first.",
                self.platform_name,
            )
            return

        if not self.account_sid or not self.api_key or not self.from_number:
            logger.error("[%s] Cannot send: missing Twilio credentials.", self.platform_name)
            return

        message_text: str = str(text)
        chunks = [message_text[i : i + CHUNK_SIZE] for i in range(0, len(message_text), CHUNK_SIZE)]
        url = TWILIO_MESSAGES_URL.format(sid=self.account_sid)

        # Normalise destination: Twilio WhatsApp numbers must be "whatsapp:+..."
        to_number = str(chat_id)
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"

        from_wa = self.from_number
        if not from_wa.startswith("whatsapp:"):
            from_wa = f"whatsapp:{from_wa}"

        for chunk in chunks:
            payload = {
                "From": from_wa,
                "To": to_number,
                "Body": chunk,
            }
            try:
                response = client.post(url, data=payload)
                response.raise_for_status()
                sid = response.json().get("sid", "unknown")
                logger.info(
                    "[%s] Message sent to %s. SID: %s",
                    self.platform_name,
                    chat_id,
                    sid,
                )
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "[%s] HTTP error sending to %s: %s – %s",
                    self.platform_name,
                    chat_id,
                    exc.response.status_code,
                    exc.response.text,
                )
            except httpx.RequestError as exc:
                logger.error(
                    "[%s] Request error sending to %s: %s",
                    self.platform_name,
                    chat_id,
                    exc,
                )
