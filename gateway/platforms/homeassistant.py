import http.server
import json
import logging
import os
import threading
from typing import Any, Callable, Optional

import httpx

from .base import BasePlatform

logger = logging.getLogger(__name__)

_DEFAULT_WEBHOOK_PORT = 8765
_CONNECT_TIMEOUT = 10.0
_REQUEST_TIMEOUT = 30.0


class _WebhookHandler(http.server.BaseHTTPRequestHandler):
    """Minimal HTTP handler that accepts POST requests from HA automations."""

    platform: "HomeAssistantPlatform"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        logger.debug("[homeassistant:webhook] " + format, *args)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length) if length > 0 else b""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

        try:
            data = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            data = {"raw": raw_body.decode("utf-8", errors="replace")}

        chat_id: str = data.get("chat_id") or data.get("source") or "ha-webhook"
        text: str = (
            data.get("text")
            or data.get("message")
            or json.dumps(data)
        )
        try:
            self.platform.handle(chat_id=chat_id, text=text)
        except Exception as exc:
            logger.error("[homeassistant:webhook] dispatch error: %s", exc)

    def do_GET(self) -> None:  # noqa: N802
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')


class HomeAssistantPlatform(BasePlatform):
    platform_name: str = "homeassistant"

    def __init__(self, config: Optional[dict] = None, on_message: Optional[Callable] = None):
        super().__init__(on_message=on_message)
        self.ha_url: str = os.getenv("HA_URL", "").rstrip("/")
        self.ha_token: str = os.getenv("HA_TOKEN", "")
        self.webhook_port: int = int(os.getenv("HA_WEBHOOK_PORT", str(_DEFAULT_WEBHOOK_PORT)))
        self._client: Optional[httpx.Client] = None
        self._webhook_server: Optional[http.server.HTTPServer] = None
        self._webhook_thread: threading.Thread = threading.Thread()  # placeholder

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self.start()

    def start(self) -> None:
        if not self.ha_url or not self.ha_token:
            missing = []
            if not self.ha_url:
                missing.append("HA_URL")
            if not self.ha_token:
                missing.append("HA_TOKEN")
            logger.warning(
                "[%s] Missing configuration variables: %s",
                self.platform_name,
                ", ".join(missing),
            )

        new_client: httpx.Client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.ha_token}",
                "Content-Type": "application/json",
            },
            timeout=_REQUEST_TIMEOUT,
        )
        self._client = new_client

        # Verify HA connection
        if self.ha_url and self.ha_token:
            try:
                response = new_client.get(f"{self.ha_url}/api/")
                response.raise_for_status()
                ha_version = response.json().get("version", "unknown")
                logger.info(
                    "[%s] Connected to Home Assistant %s at %s.",
                    self.platform_name,
                    ha_version,
                    self.ha_url,
                )
                print(
                    f"[{self.platform_name}] Connected to Home Assistant {ha_version} "
                    f"at {self.ha_url}."
                )
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "[%s] HA API check failed: %s – %s",
                    self.platform_name,
                    exc.response.status_code,
                    exc.response.text,
                )
            except httpx.RequestError as exc:
                logger.error("[%s] HA connection error: %s", self.platform_name, exc)

        self._start_webhook_listener()

    def disconnect(self) -> None:
        webhook_server = self._webhook_server
        if webhook_server is not None:
            webhook_server.shutdown()
        self._webhook_server = None

        webhook_thread = self._webhook_thread
        if webhook_thread.is_alive():
            webhook_thread.join(timeout=5)

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
                "[%s] send() called before connect()/start().", self.platform_name
            )
            return

        if not self.ha_url or not self.ha_token:
            logger.error("[%s] Cannot send: HA_URL or HA_TOKEN not set.", self.platform_name)
            return

        url = f"{self.ha_url}/api/services/notify/persistent_notification"
        payload = {
            "message": str(text),
            "title": "Pallas",
        }
        try:
            response = client.post(url, json=payload)
            response.raise_for_status()
            logger.info(
                "[%s] Persistent notification sent (chat_id=%s).", self.platform_name, chat_id
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                "[%s] HTTP error sending notification: %s – %s",
                self.platform_name,
                exc.response.status_code,
                exc.response.text,
            )
        except httpx.RequestError as exc:
            logger.error("[%s] Request error sending notification: %s", self.platform_name, exc)

    # ------------------------------------------------------------------
    # Webhook listener (background thread)
    # ------------------------------------------------------------------

    def _start_webhook_listener(self) -> None:
        """Start a local HTTP server that receives HA automation webhook POSTs."""

        # Build a handler class that has a reference back to this platform instance.
        platform_ref = self

        class BoundHandler(_WebhookHandler):
            platform = platform_ref

        try:
            server = http.server.HTTPServer(("0.0.0.0", self.webhook_port), BoundHandler)
        except OSError as exc:
            logger.error(
                "[%s] Could not bind webhook listener on port %d: %s",
                self.platform_name,
                self.webhook_port,
                exc,
            )
            return

        self._webhook_server = server
        webhook_thread = threading.Thread(
            target=server.serve_forever, daemon=True, name="ha-webhook"
        )
        self._webhook_thread = webhook_thread
        webhook_thread.start()
        logger.info(
            "[%s] Webhook listener started on port %d.", self.platform_name, self.webhook_port
        )
        print(f"[{self.platform_name}] Webhook listener on port {self.webhook_port}.")
