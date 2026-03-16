from typing import Any, List


def deliver(platform: Any, chat_id: Any, text: str):
    if hasattr(platform, "send"):
        platform.send(chat_id, text)


def chunk_message(text: str, max_len: int = 4096) -> List[str]:
    return [text[i:i + max_len] for i in range(0, len(text), max_len)]
