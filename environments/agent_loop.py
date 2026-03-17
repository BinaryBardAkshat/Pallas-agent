"""
agent_loop.py — Pallas PAR (Perception-Action-Reflection) agent loop.

Supports Anthropic, Google Gemini, OpenAI, OpenRouter, and Ollama.
"""
import uuid
from typing import Any, Callable, Dict, List, Optional

from pallas_core.provider_adapter import ProviderAdapter
from pallas_core.prompt_builder import PromptBuilder
from pallas_core.memory_store import MemoryStore
from pallas_core.trajectory import Trajectory, ToolCall
from pallas_core.usage_pricing import UsagePricing
from pallas_core.context_compressor import ContextCompressor
from pallas_core.redact import redact
from pallas_core.display import (
    console,
    print_response,
    print_tool_call,
    print_tool_result,
    print_step_header,
    print_memories,
    print_session_info,
)
from pallas_core.pallas_constants import PROVIDER_ANTHROPIC, PROVIDER_GOOGLE, DEFAULT_MODELS
from pallas_core.pallas_state import PallasState
from tools.approval import ApprovalGate


# ── Hard-coded fallback schemas for tools without a .schema property ─────────
_FALLBACK_SCHEMAS: Dict[str, Dict] = {
    "terminal": {
        "name": "terminal",
        "description": (
            "Execute any bash shell command on the user's local machine. "
            "Use for: running scripts, listing files, installing packages, git operations, "
            "compiling code, reading output of programs. You have full shell access."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The exact bash command to run (e.g. 'ls -la', 'python script.py', 'pip install requests')"
                }
            },
            "required": ["command"],
        },
    },
    "file": {
        "name": "file",
        "description": "Read, write, append, or list files on the local filesystem.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["read", "write", "append", "list"], "description": "Operation to perform"},
                "path": {"type": "string", "description": "Absolute or relative file/directory path"},
                "content": {"type": "string", "description": "Content to write or append (only for write/append actions)"},
            },
            "required": ["action", "path"],
        },
    },
    "web": {
        "name": "web",
        "description": "Search the web with DuckDuckGo or fetch the content of any URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query or full URL to fetch"}
            },
            "required": ["query"],
        },
    },
    "memory": {
        "name": "memory",
        "description": "Store or search memories across sessions. Use to remember important facts, user preferences, or past results.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["store", "search", "list"], "description": "store: save a memory | search: find relevant memories | list: show recent"},
                "content": {"type": "string", "description": "Content to store (for 'store' action)"},
                "query": {"type": "string", "description": "Search query (for 'search' action)"},
            },
            "required": ["action"],
        },
    },
    "code_exec": {
        "name": "code_exec",
        "description": "Execute Python code in a sandboxed REPL. Returns stdout, stderr, and result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"}
            },
            "required": ["code"],
        },
    },
    "todo": {
        "name": "todo",
        "description": "Manage a persistent todo list. Add, complete, list, or remove tasks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["add", "list", "complete", "remove"]},
                "task": {"type": "string", "description": "Task description (for add/complete/remove)"},
            },
            "required": ["action"],
        },
    },
}


def _schema_for_google(schema: Dict) -> Dict:
    """Convert Anthropic-style tool schema to Gemini-compatible format."""
    # Gemini uses "parameters" not "input_schema"
    converted = {
        "name": schema["name"],
        "description": schema.get("description", ""),
    }
    input_schema = schema.get("input_schema") or schema.get("parameters", {})
    if input_schema:
        converted["parameters"] = input_schema
    return converted


class AgentLoop:
    MAX_ITERATIONS = 15

    def __init__(
        self,
        provider: str = PROVIDER_ANTHROPIC,
        model: Optional[str] = None,
        human_in_loop: bool = True,
        session_id: Optional[str] = None,
    ):
        self.provider = provider
        self.model = model or DEFAULT_MODELS.get(provider)
        self.session_id = session_id or str(uuid.uuid4())

        self.state = PallasState()
        self.memory = MemoryStore()
        self.adapter = ProviderAdapter(provider)
        self.prompt_builder = PromptBuilder(memory=self.memory)
        self.trajectory = Trajectory(self.session_id)
        self.pricing = UsagePricing()
        self.compressor = ContextCompressor()
        self.approval = ApprovalGate(enabled=human_in_loop)
        self._tool_registry: Dict[str, Callable] = {}

    def register_tool(self, name: str, fn: Callable) -> None:
        self._tool_registry[name] = fn

    # ── Schema building ───────────────────────────────────────────────────────

    def _get_tool_schemas(self) -> List[Dict]:
        """Return list of tool schemas in Anthropic format (with input_schema key)."""
        schemas = []
        for name, fn in self._tool_registry.items():
            if hasattr(fn, "schema"):
                schema = fn.schema
                # Ensure input_schema key exists (some tools use 'parameters')
                if "parameters" in schema and "input_schema" not in schema:
                    schema = dict(schema)
                    schema["input_schema"] = schema.pop("parameters")
                schemas.append(schema)
            elif name in _FALLBACK_SCHEMAS:
                schemas.append(_FALLBACK_SCHEMAS[name])
        return schemas

    def _get_google_tool_schemas(self) -> List[Dict]:
        """Return tool schemas in Google Gemini format."""
        return [_schema_for_google(s) for s in self._get_tool_schemas()]

    # ── Main run loop ─────────────────────────────────────────────────────────

    def run(self, user_input: str) -> str:
        self.trajectory.add("user", user_input)
        self.state.save_message(self.session_id, "user", user_input)

        # Memory recall
        with console.status("[bold blue]◆ Recalling memories…[/bold blue]", spinner="dots"):
            relevant_memories = self.memory.search(user_input, limit=4)

        if relevant_memories:
            print_memories(relevant_memories)

        # Build system prompt with memories injected
        system = self.prompt_builder.build_system_prompt(query=user_input)

        messages = self.trajectory.to_messages()
        messages = self.compressor.compress(messages, token_budget=100_000)

        # Choose schemas based on provider
        if self.provider == PROVIDER_GOOGLE:
            tool_schemas = self._get_google_tool_schemas() or None
        else:
            tool_schemas = self._get_tool_schemas() or None

        content = ""

        for iteration in range(self.MAX_ITERATIONS):
            spinner_text = (
                f"[bold cyan]● Pallas thinking (step {iteration + 1}/{self.MAX_ITERATIONS})…[/bold cyan]"
            )
            with console.status(spinner_text, spinner="bouncingBar"):
                result = self.adapter.completion(
                    messages=messages,
                    system=system,
                    model=self.model,
                    tools=tool_schemas,
                )

            if result.get("error") and not result.get("content"):
                error_msg = f"❌ Provider error: {result['error']}"
                print_response(error_msg, title="Error")
                return error_msg

            content = result.get("content", "")
            tool_calls = result.get("tool_calls", [])
            tokens = result.get("tokens", 0)
            stop_reason = result.get("stop_reason", "end_turn")

            if tokens and self.model:
                self.pricing.record(self.model, 0, tokens)

            # No tool calls → final answer
            if not tool_calls or stop_reason == "end_turn":
                self.trajectory.add("assistant", content, tokens=tokens)
                self.state.save_message(self.session_id, "assistant", content, tokens)
                # Auto-store Q&A in memory
                if content and user_input:
                    self.memory.store(
                        content=f"Q: {user_input[:300]} | A: {content[:300]}",
                        session_id=self.session_id,
                        importance=1,
                    )
                print_response(content)
                return content

            # Execute tool calls
            executed_calls: List[ToolCall] = []
            for tc in tool_calls:
                print_tool_call(tc["name"], tc["input"])
                tool_fn = self._tool_registry.get(tc["name"])

                if not tool_fn:
                    msg = f"Tool '{tc['name']}' is not registered."
                    print_tool_result(tc["name"], msg, error=True)
                    executed_calls.append(ToolCall(name=tc["name"], input=tc["input"], error=msg))
                    continue

                if not self.approval.request(tc["name"], str(tc["input"])[:100]):
                    print_tool_result(tc["name"], "Skipped by user.", error=True)
                    executed_calls.append(
                        ToolCall(name=tc["name"], input=tc["input"], output="User declined.")
                    )
                    continue

                try:
                    output = str(tool_fn(**tc["input"]))
                    output = redact(output)
                    print_tool_result(tc["name"], output)
                    executed_calls.append(
                        ToolCall(name=tc["name"], input=tc["input"], output=output)
                    )
                except Exception as e:
                    err = f"{type(e).__name__}: {e}"
                    print_tool_result(tc["name"], err, error=True)
                    executed_calls.append(
                        ToolCall(name=tc["name"], input=tc["input"], error=err)
                    )

            self.trajectory.add(
                "assistant", content or "[tool call]", tool_calls=executed_calls, tokens=tokens
            )

            # Inject tool results as next user turn
            tool_results_block = "\n".join(
                f"[{c.name} result]: {c.output or c.error}" for c in executed_calls
            )
            messages = self.trajectory.to_messages()
            messages.append({"role": "user", "content": f"Tool results:\n{tool_results_block}"})
            messages = self.compressor.compress(messages, token_budget=100_000)

            # Update schemas for Gemini each iteration (idempotent)
            if self.provider == PROVIDER_GOOGLE:
                tool_schemas = self._get_google_tool_schemas() or None

        final = "Max iterations reached. " + (content or "(no response)")
        print_response(final)
        return final
