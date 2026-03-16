import os
from typing import Any, Callable, Optional
from gateway.platforms.base import BasePlatform

class SlackPlatform(BasePlatform):
    platform_name = "slack"

    def __init__(self, token: str = "", on_message: Optional[Callable] = None):
        super().__init__(token or os.getenv("SLACK_BOT_TOKEN", ""), on_message)

    def start(self):
        # Stub for Slack initialization using slack_sdk
        print("[Gateway] Slack listener stub: Implement using Slack Event Adapter.")

    def send(self, chat_id: Any, text: str):
        print(f"[Gateway] Slack send to {chat_id}: {text[:50]}...")
