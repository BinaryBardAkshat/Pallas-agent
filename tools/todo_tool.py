from typing import Dict, List, Optional


class TodoTool:
    name = "todo"
    description = "Manage a task list for planning and tracking work."

    def __init__(self):
        self._tasks: List[Dict[str, str]] = []
        self._counter = 0

    def __call__(self, action: str, text: str = "", task_id: str = "") -> str:
        if action == "add":
            self._counter += 1
            self._tasks.append({
                "id": str(self._counter),
                "text": text,
                "status": "pending",
            })
            return f"Task #{self._counter} added."

        elif action == "list":
            if not self._tasks:
                return "No tasks."
            return "\n".join(
                f"[{t['id']}] [{t['status']}] {t['text']}" for t in self._tasks
            )

        elif action == "done":
            for t in self._tasks:
                if t["id"] == task_id:
                    t["status"] = "done"
                    return f"Task #{task_id} marked done."
            return f"Task #{task_id} not found."

        elif action == "clear":
            self._tasks.clear()
            self._counter = 0
            return "All tasks cleared."

        return "Unknown action: add, list, done, clear."
