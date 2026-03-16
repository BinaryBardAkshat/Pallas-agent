import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from pallas_constants import DATA_DIR

CRON_DB = DATA_DIR / "cron.db"


class CronScheduler:
    def __init__(self):
        self.db = sqlite3.connect(CRON_DB, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self._init_schema()
        self._handlers: Dict[str, Callable] = {}

    def _init_schema(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                schedule TEXT NOT NULL,
                command TEXT NOT NULL,
                enabled INTEGER DEFAULT 1,
                last_run TEXT,
                next_run TEXT,
                run_count INTEGER DEFAULT 0
            )
        """)
        self.db.commit()

    def add_job(self, job_id: str, name: str, schedule: str, command: str):
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute(
            "INSERT OR REPLACE INTO jobs (id, name, schedule, command, enabled, last_run) VALUES (?,?,?,?,1,?)",
            (job_id, name, schedule, command, now)
        )
        self.db.commit()

    def list_jobs(self) -> List[Dict[str, Any]]:
        rows = self.db.execute("SELECT * FROM jobs").fetchall()
        return [dict(r) for r in rows]

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return dict(row) if row else None

    def enable_job(self, job_id: str):
        self.db.execute("UPDATE jobs SET enabled = 1 WHERE id = ?", (job_id,))
        self.db.commit()

    def disable_job(self, job_id: str):
        self.db.execute("UPDATE jobs SET enabled = 0 WHERE id = ?", (job_id,))
        self.db.commit()

    def delete_job(self, job_id: str):
        self.db.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        self.db.commit()

    def register_handler(self, name: str, fn: Callable):
        self._handlers[name] = fn

    def run_due_jobs(self):
        import schedule
        schedule.run_pending()

    def close(self):
        self.db.close()
