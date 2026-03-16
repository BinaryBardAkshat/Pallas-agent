# Architecture

## The 5-Brain System

Pallas is organized into five functional layers:

### 1. Conversation Layer
Entry point via `pallas_cli`, `gateway`, or `run_agent.py`.
Routes user input to the agent loop.

### 2. Agent Loop (`environments/agent_loop.py`)
Core Perception-Action-Reflection cycle.
- Receives user input
- Builds prompt from memory + system prompt
- Calls the LLM provider
- Parses tool calls
- Executes tools (with optional human approval)
- Loops until stop condition
- Stores result in memory and trajectory

### 3. Tool Runtime (`tools/`)
All executable capabilities: file, terminal, web, memory, code, skills.
Tools are registered into the agent loop by name.

### 4. Learning System (`pallas_core/memory_store.py`, `skills/`)
- `MemoryStore`: SQLite FTS5 full-text search over past memories
- `SOUL`: Key-value personality facts about the user
- Skills: Markdown playbooks the agent can invoke

### 5. Infrastructure Layer
- `pallas_state.py`: Config and session persistence
- `cron/`: Scheduled jobs
- `gateway/`: Multi-platform messaging
- `environments/pallas_base_env.py`: Local shell sandbox

## Data Flow

```
User Input
  --> AgentLoop.run()
    --> PromptBuilder.build_system_prompt()
    --> MemoryStore.search() [inject relevant context]
    --> ProviderAdapter.completion()
      --> Anthropic / Google / OpenAI
    --> Tool execution (if tool_calls present)
    --> Trajectory.add()
    --> MemoryStore.store() [save turn]
    --> Return final response
```

## Directory Map

| Path | Purpose |
|---|---|
| `pallas_core/` | Brain: LLM adapters, prompt, memory, trajectory |
| `pallas_cli/` | CLI interface |
| `environments/` | Agent loop and sandboxes |
| `tools/` | Callable tools |
| `gateway/` | Platform messaging adapters |
| `cron/` | Scheduled job engine |
| `pallas_state.py` | Config + session DB |
| `pallas_constants.py` | Single source of truth for paths/models |
| `skills/` | Markdown procedural memory |
| `docs/` | Developer documentation |
