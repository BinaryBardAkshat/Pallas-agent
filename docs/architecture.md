# Architecture Overview

Pallas is structured around five independent layers called **brains**. Each brain has a single responsibility. They communicate through well-defined interfaces so that any brain can be swapped independently.

---

## The 5-Brain Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Brain 1 · Conversation Layer                               │
│  pallas_cli/  ·  gateway/platforms/                         │
├─────────────────────────────────────────────────────────────┤
│  Brain 2 · Agent Loop                                       │
│  environments/agent_loop.py                                 │
├─────────────────────────────────────────────────────────────┤
│  Brain 3 · Tool Sandbox                                     │
│  tools/  ·  tools/sandbox_backends/                         │
├─────────────────────────────────────────────────────────────┤
│  Brain 4 · Learning Memory                                  │
│  pallas_core/memory_store.py  ·  pallas_core/trajectory.py  │
├─────────────────────────────────────────────────────────────┤
│  Brain 5 · Infrastructure Layer                             │
│  tools/sandbox_backends/{local,docker,ssh,modal}.py         │
└─────────────────────────────────────────────────────────────┘
```

### Brain 1 — Conversation Layer

Entry points that accept human input and surface agent output. The CLI (`pallas_cli/`) handles interactive terminal sessions and one-shot queries. The Gateway (`gateway/`) handles platform bots (Telegram, Discord, Slack, WhatsApp, etc.). Both funnel messages into the same `AgentLoop`.

### Brain 2 — Agent Loop

`environments/agent_loop.py` is the core reasoning engine. It implements a **Perception-Action-Reflection (PAR)** cycle. On each iteration it calls the LLM, parses tool calls, dispatches them, feeds results back, and repeats until the model stops calling tools or `MAX_ITERATIONS = 15` is hit.

### Brain 3 — Tool Sandbox

Every capability exposed to the model lives here. Tools are registered by name as callables on the `AgentLoop`. Each tool exposes a `.schema` property in Anthropic `input_schema` format. The `ApprovalGate` wraps every tool call — in `human_in_loop` mode the operator must confirm before execution.

### Brain 4 — Learning Memory

`MemoryStore` (FTS5 SQLite) stores Q&A pairs after each session turn. On the next user message, the top-3 relevant memories are retrieved and passed to `PromptBuilder`. `Trajectory` stores the full message history for the current session. `PallasState` persists cross-session config (default provider, last session ID, etc.).

### Brain 5 — Infrastructure Layer

The `SandboxBackend` abstraction in `tools/sandbox_backends/` decouples command execution from the rest of the system. The backend is selected at runtime by the `PALLAS_SANDBOX` environment variable. This means Brain 3 tools call `backend.execute(cmd)` without knowing whether they are running locally, inside Docker, over SSH, or on Modal.

---

## Data Flow

```
User Input
    │
    ▼
Conversation Layer (CLI / Gateway)
    │  raw text
    ▼
AgentLoop.run(user_input)
    │
    ├─ MemoryStore.search(user_input)       ← top-3 relevant memories
    ├─ PromptBuilder.build_system_prompt()  ← system prompt with skills + memory
    ├─ Trajectory.to_messages()             ← full conversation history
    └─ ContextCompressor.compress()         ← trim to 100k token budget
         │
         ▼
    ProviderAdapter.completion(messages, system, model, tools)
         │  LLM response
         ▼
    Parse content + tool_calls
         │
         ├─ [no tool calls] → print response, store memory, return
         │
         └─ [tool calls] ──► ApprovalGate.request(name, preview)
                                  │  approved
                                  ▼
                             tool_fn(**input)   ← dispatched via SandboxBackend
                                  │  stdout/stderr/exit_code
                                  ▼
                             Trajectory.add(tool_results)
                                  │
                                  └─ loop back to LLM ↑
```

---

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `environments/agent_loop.py` | PAR cycle, tool dispatch, iteration cap |
| `pallas_core/provider_adapter.py` | Normalize requests/responses across LLM providers |
| `pallas_core/prompt_builder.py` | Assemble system prompt (base directives + context) |
| `pallas_core/memory_store.py` | FTS5 SQLite store for episodic memory |
| `pallas_core/trajectory.py` | Per-session message history buffer |
| `pallas_core/context_compressor.py` | Drop oldest messages when token budget exceeded |
| `pallas_core/toolsets.py` | Register all default tools onto an AgentLoop instance |
| `pallas_core/pallas_state.py` | Persist cross-session key/value config |
| `pallas_core/skill_commands.py` | Load and invoke SKILL.md files |
| `pallas_core/usage_pricing.py` | Track token usage and estimated cost per model |
| `pallas_core/auxiliary_client.py` | Lightweight LLM calls for summarization/insights |
| `pallas_core/prompt_caching.py` | Inject Anthropic cache_control breakpoints |
| `tools/approval.py` | Human-in-the-loop confirmation gate |
| `tools/sandbox_backends/` | Pluggable execution backends (local/docker/ssh/modal) |
| `gateway/session.py` | Session routing for platform bots |
| `gateway/platforms/base.py` | Abstract platform interface |
| `pallas_cli/main.py` | CLI command definitions |
| `pallas_cli/commands.py` | Interactive chat session logic |

---

## How Providers Work

`ProviderAdapter` is the only place that knows about provider-specific API shapes. Every other module talks to it through a single normalized contract:

```python
result = adapter.completion(
    messages=[{"role": "user", "content": "..."}],
    system="You are Pallas...",
    model="claude-sonnet-4-6",
    tools=[{
        "name": "terminal",
        "description": "Execute bash commands",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    }]
)
# Returns:
# {
#   "content": "Here is the result...",
#   "tool_calls": [{"name": "terminal", "input": {"command": "ls -la"}}],
#   "tokens": 142,
#   "stop_reason": "tool_use",
#   "error": None
# }
```

Internally the adapter translates into each provider's wire format. Anthropic receives `tools` directly; Google Gemini receives them as `function_declarations`; OpenAI receives them as `functions`. The caller never sees the difference.

### Auxiliary Client

`pallas_core/auxiliary_client.py` provides a second, lighter LLM call path for background tasks like context summarization, insight extraction, and skill matching. It uses `AUX_MODELS` (smaller, cheaper models) from `pallas_constants.py` so the primary reasoning loop stays on the full-power model.

### Prompt Caching

When using Anthropic, `pallas_core/prompt_caching.py` injects `cache_control` breakpoints into the message array. This caches the static portion of the system prompt and tool schemas across turns, reducing latency and cost significantly on long sessions.

### Provider Constants

All model IDs, endpoint URLs, and routing preferences live in `pallas_core/pallas_constants.py`. To add a new provider, add its constants there and add a branch in `ProviderAdapter`.
