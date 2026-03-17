import json
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple

from pallas_core.pallas_constants import SESSIONS_DB_PATH


class CheckpointManager:
    """Save/restore agent state snapshots for long-running tasks."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self._db_path = str(SESSIONS_DB_PATH)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoints (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    label TEXT NOT NULL,
                    messages_json TEXT NOT NULL,
                    trajectory_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def save(self, label: str, trajectory: Any, messages: List[dict]) -> str:
        """Save a checkpoint and return its checkpoint_id."""
        checkpoint_id = str(uuid.uuid4())
        messages_json = json.dumps(messages, default=str)

        # trajectory may be a Trajectory object or raw list/dict
        if hasattr(trajectory, "__dict__"):
            trajectory_data = trajectory.__dict__
        elif isinstance(trajectory, (list, dict)):
            trajectory_data = trajectory
        else:
            trajectory_data = {"raw": str(trajectory)}

        trajectory_json = json.dumps(trajectory_data, default=str)

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO checkpoints (id, session_id, label, messages_json, trajectory_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (checkpoint_id, self.session_id, label, messages_json, trajectory_json),
            )
            conn.commit()

        return checkpoint_id

    def list(self, session_id: Optional[str] = None) -> List[dict]:
        """Return all checkpoints for the given (or current) session."""
        sid = session_id or self.session_id
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, session_id, label, created_at FROM checkpoints WHERE session_id = ? ORDER BY created_at DESC",
                (sid,),
            ).fetchall()
        return [dict(row) for row in rows]

    def restore(self, checkpoint_id: str) -> Tuple[List[dict], Any]:
        """Return (messages, trajectory_data) for the given checkpoint_id."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT messages_json, trajectory_json FROM checkpoints WHERE id = ?",
                (checkpoint_id,),
            ).fetchone()

        if row is None:
            raise KeyError(f"Checkpoint not found: {checkpoint_id}")

        messages: List[dict] = json.loads(row["messages_json"])
        trajectory_data: Any = json.loads(row["trajectory_json"])
        return messages, trajectory_data

    def auto_checkpoint(self, agent_loop: Any, every_n_steps: int = 5):
        """Wrap agent_loop to auto-save a checkpoint every N tool calls."""
        original_run = agent_loop.run
        manager = self

        def wrapped_run(user_input: str) -> str:
            step_counter = {"n": 0}
            original_execute = getattr(agent_loop, "_execute_tool", None)

            # Wrap internal tool dispatch if the method exists
            if original_execute is not None:
                def counting_execute(*args, **kwargs):
                    result = original_execute(*args, **kwargs)
                    step_counter["n"] += 1
                    if step_counter["n"] % every_n_steps == 0:
                        try:
                            messages = agent_loop.trajectory.to_messages() if hasattr(agent_loop, "trajectory") else []
                            manager.save(
                                label=f"auto-step-{step_counter['n']}",
                                trajectory=agent_loop.trajectory if hasattr(agent_loop, "trajectory") else {},
                                messages=messages,
                            )
                        except Exception:
                            pass
                    return result

                agent_loop._execute_tool = counting_execute

            result = original_run(user_input)

            # Save a final checkpoint after the run completes
            try:
                messages = agent_loop.trajectory.to_messages() if hasattr(agent_loop, "trajectory") else []
                manager.save(
                    label="auto-final",
                    trajectory=agent_loop.trajectory if hasattr(agent_loop, "trajectory") else {},
                    messages=messages,
                )
            except Exception:
                pass

            return result

        agent_loop.run = wrapped_run

    def cleanup_old(self):
        """Delete checkpoints older than 7 days."""
        cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat()
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM checkpoints WHERE created_at < ?",
                (cutoff,),
            )
            conn.commit()
