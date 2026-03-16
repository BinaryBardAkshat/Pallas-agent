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
    print_response,
    print_tool_call,
    print_tool_result,
    print_thinking,
    print_memories,
)
from pallas_constants import DEFAULT_MODELS, PROVIDER_ANTHROPIC
from pallas_state import PallasState
from tools.approval import ApprovalGate


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

    def register_tool(self, name: str, fn: Callable):
        self._tool_registry[name] = fn

    def _get_tool_schemas(self) -> List[Dict]:
        return []

    def run(self, user_input: str) -> str:
        self.trajectory.add("user", user_input)
        self.state.save_message(self.session_id, "user", user_input)

        relevant_memories = self.memory.search(user_input, limit=3)
        if relevant_memories:
            print_memories(relevant_memories)

        messages = self.trajectory.to_messages()
        messages = self.compressor.compress(messages, token_budget=100_000)
        system = self.prompt_builder.build_system_prompt()

        content = ""

        for iteration in range(self.MAX_ITERATIONS):
            print_thinking(f"Step {iteration + 1}...")

            result = self.adapter.completion(
                messages=messages,
                system=system,
                model=self.model,
                tools=self._get_tool_schemas() or None,
            )

            if result.get("error") and not result.get("content"):
                error_msg = f"Provider error: {result['error']}"
                print_response(error_msg, title="Error")
                return error_msg

            content = result.get("content", "")
            tool_calls = result.get("tool_calls", [])
            tokens = result.get("tokens", 0)
            stop_reason = result.get("stop_reason", "end_turn")

            if tokens and self.model:
                self.pricing.record(self.model, 0, tokens)

            if not tool_calls or stop_reason == "end_turn":
                self.trajectory.add("assistant", content, tokens=tokens)
                self.state.save_message(self.session_id, "assistant", content, tokens)
                self.memory.store(
                    content=f"Q: {user_input[:200]} | A: {content[:200]}",
                    session_id=self.session_id,
                    importance=1,
                )
                print_response(content)
                return content

            executed_calls = []
            for tc in tool_calls:
                print_tool_call(tc["name"], tc["input"])
                tool_fn = self._tool_registry.get(tc["name"])

                if not tool_fn:
                    executed_calls.append(
                        ToolCall(name=tc["name"], input=tc["input"], error="Tool not found.")
                    )
                    continue

                if not self.approval.request(tc["name"], str(tc["input"])[:80]):
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
                    err = str(e)
                    print_tool_result(tc["name"], err, error=True)
                    executed_calls.append(
                        ToolCall(name=tc["name"], input=tc["input"], error=err)
                    )

            self.trajectory.add(
                "assistant", content or "[tool call]", tool_calls=executed_calls, tokens=tokens
            )

            tool_results_block = "\n".join(
                f"[{c.name}]: {c.output or c.error}" for c in executed_calls
            )
            messages = self.trajectory.to_messages()
            messages.append({"role": "user", "content": f"Tool results:\n{tool_results_block}"})
            messages = self.compressor.compress(messages, token_budget=100_000)

        final = "Max iterations reached. Last response: " + (content or "")
        print_response(final)
        return final
