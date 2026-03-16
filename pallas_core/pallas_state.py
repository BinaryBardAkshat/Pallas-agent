import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional
from .pallas_constants import CONFIG_PATH, SESSIONS_DB_PATH, MEMORY_DB_PATH
from .pallas_time import timestamp

class PallasState:
    def __init__(self):
        self.config_path = CONFIG_PATH
        self.db_path = SESSIONS_DB_PATH
        self.memory_db_path = MEMORY_DB_PATH
        self._init_db()
        self.config = self._load_config()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, metadata TEXT, created_at REAL)"
        )
        conn.commit()
        conn.close()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_config(self, config: Dict[str, Any]):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
        self.config = config

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config(self.config)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT metadata FROM sessions WHERE id = ?", (session_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return None

    def save_session(self, session_id: str, metadata: Dict[str, Any]):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO sessions (id, metadata, created_at) VALUES (?, ?, ?)",
            (session_id, json.dumps(metadata), timestamp()),
        )
        conn.commit()
        conn.close()
