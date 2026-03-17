import threading
import uuid
from typing import List, Optional

from pallas_core.pallas_constants import PROVIDER_ANTHROPIC, DEFAULT_MODELS


class DelegateTool:
    """Spawn a specialized sub-agent to handle a subtask."""

    schema = {
        "name": "delegate",
        "description": "Spawn a specialized sub-agent to handle a subtask. Use for parallelizable or complex sub-tasks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "The task for the sub-agent"},
                "tools": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tool names to give sub-agent (default: all)",
                },
                "provider": {"type": "string", "description": "Optional provider override"},
                "model": {"type": "string", "description": "Optional model override"},
            },
            "required": ["task"],
        },
    }

    def __call__(
        self,
        task: str,
        tools: Optional[List[str]] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ) -> str:
        try:
            # Deferred import to avoid circular imports
            from environments.agent_loop import AgentLoop
            from pallas_core.toolsets import get_toolset

            sub_provider = provider or PROVIDER_ANTHROPIC
            sub_model = model or DEFAULT_MODELS.get(sub_provider)
            sub_session_id = str(uuid.uuid4())

            loop = AgentLoop(
                provider=sub_provider,
                model=sub_model,
                human_in_loop=False,
                session_id=sub_session_id,
            )

            # Register tools: filtered subset or full default toolset
            toolset = get_toolset(tools)
            for name, tool_fn in toolset.items():
                loop.register_tool(name, tool_fn)

            result_container: dict = {}
            exception_container: dict = {}

            def _run():
                try:
                    result_container["result"] = loop.run(task)
                except Exception as e:
                    exception_container["error"] = str(e)

            thread = threading.Thread(target=_run, daemon=True)
            thread.start()
            thread.join(timeout=300)  # 5-minute timeout

            if thread.is_alive():
                return "ERROR: Sub-agent timed out after 5 minutes."

            if exception_container:
                return f"ERROR: Sub-agent raised an exception: {exception_container['error']}"

            raw: str = result_container.get("result") or ""
            return raw[:10000]

        except Exception as e:
            return f"ERROR: Failed to spawn sub-agent: {str(e)}"
