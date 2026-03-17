import json
import logging
import os
import subprocess
import threading
from typing import Any, Callable, List, Optional

from .base import BasePlatform

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1600


class SignalPlatform(BasePlatform):
    platform_name: str = "signal"

    def __init__(self, phone_number: str = "", on_message: Optional[Callable] = None):
        super().__init__(token=phone_number, on_message=on_message)
        self.phone_number: str = phone_number or os.getenv("SIGNAL_PHONE_NUMBER", "")
        self.cli_path: str = os.getenv("SIGNAL_CLI_PATH", "signal-cli")
        self._stop_event: threading.Event = threading.Event()
        self._recv_thread: threading.Thread = threading.Thread()  # placeholder, never started

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self.start()

    def start(self) -> None:
        if not self.phone_number:
            logger.warning("[%s] SIGNAL_PHONE_NUMBER is not set.", self.platform_name)

        # Verify signal-cli is available
        try:
            result = subprocess.run(
                [self.cli_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                logger.error(
                    "[%s] signal-cli exited with code %d: %s",
                    self.platform_name,
                    result.returncode,
                    result.stderr.strip(),
                )
            else:
                version = result.stdout.strip() or result.stderr.strip()
                logger.info("[%s] signal-cli found: %s", self.platform_name, version)
                print(
                    f"[{self.platform_name}] signal-cli ready ({version}). "
                    f"Account: {self.phone_number}"
                )
        except FileNotFoundError:
            logger.error(
                "[%s] signal-cli not found at path: %s", self.platform_name, self.cli_path
            )
            print(
                f"[{self.platform_name}] ERROR: signal-cli not found at '{self.cli_path}'. "
                "Set SIGNAL_CLI_PATH or install signal-cli."
            )
            return
        except subprocess.TimeoutExpired:
            logger.error("[%s] signal-cli --version timed out.", self.platform_name)
            return

        # Start background receive loop
        self._stop_event.clear()
        recv_thread = threading.Thread(
            target=self._receive_loop, daemon=True, name="signal-receive"
        )
        self._recv_thread = recv_thread
        recv_thread.start()

    def disconnect(self) -> None:
        self._stop_event.set()
        recv_thread = self._recv_thread
        if recv_thread.is_alive():
            recv_thread.join(timeout=5)
        logger.info("[%s] Disconnected.", self.platform_name)
        print(f"[{self.platform_name}] Disconnected.")

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------

    def send(self, chat_id: Any, text: str) -> None:
        if not self.phone_number:
            logger.error("[%s] Cannot send: SIGNAL_PHONE_NUMBER not set.", self.platform_name)
            return

        message_text: str = str(text)
        chunks: List[str] = [
            message_text[i : i + CHUNK_SIZE] for i in range(0, len(message_text), CHUNK_SIZE)
        ]

        for chunk in chunks:
            cmd = [
                self.cli_path,
                "-u", self.phone_number,
                "send",
                "-r", str(chat_id),
                "-m", chunk,
            ]
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    logger.error(
                        "[%s] send failed (exit %d): %s",
                        self.platform_name,
                        result.returncode,
                        result.stderr.strip(),
                    )
                else:
                    logger.info("[%s] Message sent to %s.", self.platform_name, chat_id)
            except FileNotFoundError:
                logger.error(
                    "[%s] signal-cli not found at '%s'.", self.platform_name, self.cli_path
                )
            except subprocess.TimeoutExpired:
                logger.error(
                    "[%s] send timed out for recipient %s.", self.platform_name, chat_id
                )

    # ------------------------------------------------------------------
    # Receive loop (background thread)
    # ------------------------------------------------------------------

    def _receive_loop(self) -> None:
        """Run signal-cli receive --output=json in a long-running subprocess."""
        if not self.phone_number:
            logger.error(
                "[%s] _receive_loop aborted: SIGNAL_PHONE_NUMBER not set.", self.platform_name
            )
            return

        cmd = [
            self.cli_path,
            "-u", self.phone_number,
            "receive",
            "--output=json",
        ]

        while not self._stop_event.is_set():
            proc: Optional[subprocess.Popen[str]] = None
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout = proc.stdout
                if stdout is not None:
                    for line in stdout:
                        if self._stop_event.is_set():
                            break
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            logger.debug(
                                "[%s] Non-JSON line: %s", self.platform_name, line
                            )
                            continue
                        self._dispatch(data)

                proc.wait()
                if proc.returncode != 0 and not self._stop_event.is_set():
                    stderr_pipe = proc.stderr
                    stderr_out = stderr_pipe.read() if stderr_pipe is not None else ""
                    logger.warning(
                        "[%s] receive exited with code %d: %s",
                        self.platform_name,
                        proc.returncode,
                        stderr_out.strip(),
                    )
            except FileNotFoundError:
                logger.error(
                    "[%s] signal-cli not found in receive loop.", self.platform_name
                )
                self._stop_event.wait(timeout=30)
            except Exception as exc:
                logger.error("[%s] Receive loop error: %s", self.platform_name, exc)
                if not self._stop_event.is_set():
                    self._stop_event.wait(timeout=5)
            finally:
                if proc is not None and proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()

    def _dispatch(self, data: dict) -> None:
        """Parse a signal-cli JSON envelope and call self.handle()."""
        try:
            envelope: dict = data.get("envelope", data)
            sender: str = (
                envelope.get("source")
                or envelope.get("sourceNumber")
                or envelope.get("sourceName")
                or "unknown"
            )
            data_message: dict = envelope.get("dataMessage") or {}
            sync_message: dict = envelope.get("syncMessage") or {}
            sent_message: dict = sync_message.get("sentMessage") or {}
            body: str = (
                data_message.get("message")
                or sent_message.get("message")
                or ""
            )
            if body:
                self.handle(chat_id=sender, text=body)
        except Exception as exc:
            logger.error("[%s] Error dispatching message: %s", self.platform_name, exc)
