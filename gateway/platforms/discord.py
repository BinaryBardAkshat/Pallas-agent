import os
from typing import Any, Callable, Optional
from gateway.platforms.base import BasePlatform

class DiscordPlatform(BasePlatform):
    platform_name = "discord"

    def __init__(self, token: str = "", on_message: Optional[Callable] = None):
        super().__init__(token or os.getenv("DISCORD_BOT_TOKEN", ""), on_message)

    def start(self):
        # Stub for discord initialization using discord.py
        print("[Gateway] Discord listener stub: Implement using discord.py client.")

    def send(self, chat_id: Any, text: str):
        print(f"[Gateway] Discord send to {chat_id}: {text[:50]}...")
