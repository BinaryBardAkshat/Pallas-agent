import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from .pallas_constants import (
    MEMORY_DB_PATH,
    PROVIDER_ANTHROPIC,
    PROVIDER_GOOGLE,
    PROVIDER_OPENAI,
    PROVIDER_OPENROUTER,
    PROVIDER_OLLAMA,
)


class MemoryStore:
    def __init__(self):
        self.db = sqlite3.connect(MEMORY_DB_PATH, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                importance INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                source TEXT DEFAULT 'agent'
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts
                USING fts5(content, tags, content=memories, content_rowid=id);

            CREATE TABLE IF NOT EXISTS soul (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            );
        """)
        self.db.commit()

    def store(
        self,
        content: str,
        session_id: str = "",
        tags: List[str] = None,
        importance: int = 1,
        source: str = "agent",
    ) -> int:
        from .pallas_time import timestamp
        tags_json = json.dumps(tags or [])
        cur = self.db.execute(
            "INSERT INTO memories (session_id, content, tags, importance, created_at, source) VALUES (?,?,?,?,?,?)",
            (session_id, content, tags_json, importance, timestamp(), source)
        )
        rowid = cur.lastrowid
        self.db.execute(
            "INSERT INTO memories_fts (rowid, content, tags) VALUES (?,?,?)",
            (rowid, content, tags_json)
        )
        self.db.commit()
        return rowid

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        import re
        clean_query = re.sub(r'[^\w\s]', ' ', query).strip()
        if not clean_query:
            return []

        fts_query = " OR ".join(f'"{word}"*' for word in clean_query.split())
        
        try:
            rows = self.db.execute(
                "SELECT m.* FROM memories m JOIN memories_fts f ON m.id = f.rowid WHERE memories_fts MATCH ? ORDER BY rank LIMIT ?",
                (fts_query, limit)
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        rows = self.db.execute(
            "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def set_soul_key(self, key: str, value: str):
        from .pallas_time import timestamp
        self.db.execute(
            "INSERT OR REPLACE INTO soul (key, value, updated_at) VALUES (?,?,?)",
            (key, value, timestamp())
        )
        self.db.commit()

    def get_soul_key(self, key: str) -> Optional[str]:
        row = self.db.execute("SELECT value FROM soul WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def get_full_soul(self) -> Dict[str, str]:
        rows = self.db.execute("SELECT key, value FROM soul").fetchall()
        return {r["key"]: r["value"] for r in rows}

    def close(self):
        self.db.close()
