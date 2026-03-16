import json
from typing import Any, Dict, List, Optional
from pallas_core.memory_store import MemoryStore


class MemoryTool:
    name = "memory"
    description = "Store or retrieve memories across sessions."

    def __init__(self, store: Optional[MemoryStore] = None):
        self.store = store or MemoryStore()

    def __call__(self, action: str, content: str = "", query: str = "", tags: str = "") -> str:
        if action == "store":
            tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
            rowid = self.store.store(content=content, tags=tag_list)
            return f"Memory stored (id={rowid})."

        elif action == "search":
            results = self.store.search(query)
            if not results:
                return "No memories found."
            return "\n".join(f"[{r['id']}] {r['content']}" for r in results)

        elif action == "recent":
            results = self.store.get_recent(limit=5)
            if not results:
                return "No memories yet."
            return "\n".join(f"[{r['id']}] {r['content']}" for r in results)

        elif action == "soul_set":
            key, _, value = content.partition("=")
            self.store.set_soul_key(key.strip(), value.strip())
            return f"SOUL key '{key.strip()}' updated."

        elif action == "soul_get":
            return self.store.get_soul_key(content) or "(not set)"

        return "Unknown action. Use: store, search, recent, soul_set, soul_get."
