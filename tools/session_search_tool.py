from typing import Any, Dict, List
from pallas_core.memory_store import MemoryStore


class SessionSearchTool:
    name = "session_search"
    description = "Search across past session conversations by keyword."

    def __init__(self, store: MemoryStore = None):
        self.store = store or MemoryStore()

    def __call__(self, query: str, limit: int = 5) -> str:
        results = self.store.search(query, limit=limit)
        if not results:
            return f"No past sessions match '{query}'."
        lines = []
        for r in results:
            lines.append(f"[{r.get('session_id', '?')}] {r['content'][:150]}")
        return "\n".join(lines)
