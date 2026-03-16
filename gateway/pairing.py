import uuid
from typing import Dict, Optional


class PairingManager:
    def __init__(self):
        self._pairs: Dict[str, str] = {}

    def get_session_id(self, platform: str, user_id: str) -> str:
        key = f"{platform}:{user_id}"
        if key not in self._pairs:
            self._pairs[key] = str(uuid.uuid5(uuid.NAMESPACE_DNS, key))
        return self._pairs[key]

    def unpair(self, platform: str, user_id: str):
        key = f"{platform}:{user_id}"
        self._pairs.pop(key, None)

    def list_pairs(self) -> Dict[str, str]:
        return dict(self._pairs)
