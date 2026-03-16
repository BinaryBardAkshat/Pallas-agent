from typing import Any, Dict


class AdapterSession:
    def __init__(self, session_id: str, metadata: Dict[str, Any] = None):
        self.session_id = session_id
        self.metadata = metadata or {}
        self.active = True

    def close(self):
        self.active = False
