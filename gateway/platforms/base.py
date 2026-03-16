from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class BasePlatform(ABC):
    platform_name: str = "base"

    def __init__(self, token: str = "", on_message: Optional[Callable] = None):
        self.token = token
        self.on_message = on_message

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send(self, chat_id: Any, text: str):
        pass

    def handle(self, chat_id: Any, text: str) -> str:
        if self.on_message:
            return self.on_message(chat_id=chat_id, text=text, platform=self.platform_name)
        return "(no handler)"
