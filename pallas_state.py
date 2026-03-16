import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional
from pallas_constants import CONFIG_PATH, SESSIONS_DB_PATH
from pallas_time import timestamp

class PallasState:
    def __init__(self):
        self.config = self._load_config()
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(SESSIONS_DB_PATH) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        role TEXT,
                        content TEXT,
                        tokens INTEGER,
                        timestamp TEXT
                    )
                ''')
        except Exception:
            pass

    def _load_config(self) -> Dict[str, Any]:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        return {
            "default_provider": None,
            "active_session": None,
            "skills_enabled": True
        }

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save()

    def save_message(self, session_id: str, role: str, content: str, tokens: int = 0):
        try:
            with sqlite3.connect(SESSIONS_DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO messages (session_id, role, content, tokens, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (session_id, role, content, tokens, timestamp())
                )
        except Exception as e:
            pass
