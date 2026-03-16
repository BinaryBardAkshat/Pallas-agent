import hashlib
from typing import Dict, Optional


class PromptCache:
    def __init__(self, max_entries: int = 100):
        self._cache: Dict[str, str] = {}
        self._max_entries = max_entries

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    def get(self, prompt: str) -> Optional[str]:
        return self._cache.get(self._hash(prompt))

    def put(self, prompt: str, response: str):
        if len(self._cache) >= self._max_entries:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        self._cache[self._hash(prompt)] = response

    def clear(self):
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)
