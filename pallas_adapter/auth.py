from typing import Optional


class PallasAuth:
    def __init__(self, token: Optional[str] = None):
        self._token = token

    def validate(self, token: str) -> bool:
        if not self._token:
            return True
        return token == self._token

    def set_token(self, token: str):
        self._token = token
