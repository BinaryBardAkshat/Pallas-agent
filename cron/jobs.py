from typing import Any, Dict
from environments.agent_loop import AgentLoop
from pallas_core.pallas_constants import PROVIDER_ANTHROPIC


def daily_summary_job(agent: AgentLoop = None) -> str:
    if not agent:
        agent = AgentLoop(provider=PROVIDER_ANTHROPIC, human_in_loop=False)
    return agent.run("Give me a brief summary of what we discussed today and any pending tasks.")


def memory_cleanup_job(agent: AgentLoop = None) -> str:
    from pallas_core.memory_store import MemoryStore
    store = MemoryStore()
    recent = store.get_recent(limit=100)
    return f"Memory cleanup: {len(recent)} memories indexed."


BUILTIN_JOBS: Dict[str, Any] = {
    "daily_summary": {
        "fn": daily_summary_job,
        "schedule": "daily",
        "description": "Summarizes the day's work at end of day.",
    },
    "memory_cleanup": {
        "fn": memory_cleanup_job,
        "schedule": "weekly",
        "description": "Runs memory indexing and cleanup.",
    },
}
