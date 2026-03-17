# AgentLoop Internals

This document covers the `AgentLoop` class in `environments/agent_loop.py` — the core reasoning engine that implements the Perception-Action-Reflection (PAR) cycle.

---

## The PAR Cycle

Every call to `AgentLoop.run(user_input)` executes the following cycle:

```
┌──────────────────────────────────────────────────┐
│  PERCEPTION                                       │
│  - Retrieve top-3 relevant memories (FTS5)        │
│  - Build system prompt                            │
│  - Load trajectory (message history)              │
│  - Compress context to token budget               │
└───────────────────┬──────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────┐
│  ACTION                                           │
│  - Call LLM via ProviderAdapter                   │
│  - Parse response: content + tool_calls           │
│  - If no tool calls → emit response, store memory │
│  - If tool calls → ApprovalGate → execute         │
└───────────────────┬──────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────┐
│  REFLECTION                                       │
│  - Append tool results to Trajectory              │
│  - Feed results back to LLM in next iteration     │
│  - If stop_reason == "end_turn" → exit loop       │
└──────────────────────────────────────────────────┘
```

This cycle repeats up to `MAX_ITERATIONS = 15` times per user message.

---

## Max Iterations

```python
class AgentLoop:
    MAX_ITERATIONS = 15
```

The cap prevents infinite loops when a model keeps calling tools without reaching a conclusion. On the 15th iteration, if the model still has not returned a final text response, the loop terminates with:

```
Max iterations reached. Last response: <last content>
```

In practice, most tasks complete in 1-5 iterations. Complex multi-step tasks (scaffolding a project, running a full test suite, researching a topic) may use 8-12. If you consistently hit the cap, the task should be broken into smaller sub-tasks.

---

## Context Compression

Before each LLM call, the message history is compressed to fit within the token budget:

```python
messages = self.compressor.compress(messages, token_budget=100_000)
```

`ContextCompressor` in `pallas_core/context_compressor.py` trims the oldest messages when the estimated token count exceeds `100_000`. It preserves:
- The most recent user message (always)
- The most recent assistant responses
- Tool results from the current turn

This ensures the model always has the latest context without exceeding provider limits.

---

## Trajectory Tracking

`Trajectory` in `pallas_core/trajectory.py` is the in-memory session buffer. It stores every message exchange in the current session as structured objects:

```python
@dataclass
class ToolCall:
    name: str
    input: dict
    output: str | None = None
    error: str | None = None

class Trajectory:
    def add(self, role: str, content: str, tool_calls=None, tokens=0): ...
    def to_messages(self) -> List[Dict]: ...
```

`to_messages()` converts the trajectory into the flat `[{"role": ..., "content": ...}]` format expected by LLM APIs.

---

## Session Persistence

Each session has a unique UUID assigned at initialization:

```python
self.session_id = session_id or str(uuid.uuid4())
```

Every user and assistant message is saved to SQLite via `PallasState.save_message()`:

```python
self.state.save_message(self.session_id, "user", user_input)
self.state.save_message(self.session_id, "assistant", content, tokens)
```

Sessions can be resumed by passing the session ID:

```bash
pallas start --session <uuid>
```

Past sessions are searchable via `pallas_core/session_search_tool.py` using FTS5 full-text search.

---

## Memory Storage

After every successful response, a Q&A summary is stored in `MemoryStore`:

```python
self.memory.store(
    content=f"Q: {user_input[:200]} | A: {content[:200]}",
    session_id=self.session_id,
    importance=1,
)
```

This creates a growing episodic memory index. On the next turn, the FTS5 search surfaces the most relevant past interactions to give the agent continuity across sessions.

---

## Tool Dispatch

Tool dispatch is a tight try/except loop:

```python
try:
    output = str(tool_fn(**tc["input"]))
    output = redact(output)              # strip secrets from output
    print_tool_result(tc["name"], output)
    executed_calls.append(ToolCall(name=tc["name"], input=tc["input"], output=output))
except Exception as e:
    err = str(e)
    print_tool_result(tc["name"], err, error=True)
    executed_calls.append(ToolCall(name=tc["name"], input=tc["input"], error=err))
```

Tool errors do not crash the loop. The error string is passed back to the model as the tool result, allowing it to adapt (try a different command, ask for clarification, etc.).

`redact()` in `pallas_core/redact.py` strips common secret patterns (API keys, tokens) from tool output before it enters the conversation history.

---

## Usage Pricing

Token counts from each LLM response are tracked:

```python
if tokens and self.model:
    self.pricing.record(self.model, 0, tokens)
```

`UsagePricing` in `pallas_core/usage_pricing.py` stores a running total per model and can compute estimated cost based on published per-token rates.
