# Prompt Assembly

Every time `AgentLoop.run()` starts a new turn, it calls `PromptBuilder.build_system_prompt()` to construct the system prompt sent to the LLM. This document explains what goes into that prompt and how each part is assembled.

---

## System Prompt Structure

The final system prompt is a single string concatenated from these sections:

```
[1] Base directives
[2] Current context (optional)
```

At runtime in `agent_loop.py`, relevant memories retrieved from `MemoryStore` are available as local variables and can be surfaced in logs and display, though the current `PromptBuilder` implementation keeps the system prompt lean. The prompt is designed to be injected once and cached by the provider (see Prompt Caching below).

### Base Directives

Defined in `pallas_core/prompt_builder.py`:

```python
base_prompt = (
    "You are Pallas, a self-evolving autonomous AI agent embedded in a local environment. "
    "Your goal is to execute tasks with precision, safety, and strategic wisdom by ACTUALLY DOING THEM. "
    "You operate in a Perception-Action-Reflection cycle.\n\n"
    "CRITICAL DIRECTIVES:\n"
    "1. You have FULL ACCESS to the user's computer via your available tools.\n"
    "2. NEVER say you 'do not have direct access to the local file system'. USE YOUR TOOLS.\n"
    "3. When asked to create files or run code, DO NOT explain. EXECUTE via tool calls.\n"
    "4. DO NOT write markdown code blocks trying to invoke tools. Use API function calls.\n"
    "5. Assume actions are allowed. The approval gate will intercept if needed."
)
```

These directives enforce an **action-first** posture. Without them, models often default to describing what they would do rather than doing it.

---

## How Skills Are Injected

Skills live in `~/.pallas/skills/<skill-name>/SKILL.md`. They are loaded by `SkillCommands` from `pallas_core/skill_commands.py`.

When a skill is invoked (via `SkillManagerTool` or directly), the skill content is prepended to the user message rather than the system prompt:

```python
def invoke_skill_prompt(self, name: str, user_query: str) -> str:
    content = self.get_skill(name)
    return (
        f"You have a skill called '{name}'. Follow these instructions precisely:\n\n"
        f"{content}\n\n"
        f"User request: {user_query}"
    )
```

This approach means:
- The base system prompt stays short and cacheable
- Skills are only loaded when needed, saving tokens
- Skills can be updated without restarting the agent

To add a skill to every session automatically, copy its `SKILL.md` into `~/.pallas/skills/` and trigger it from your opening message, or extend `PromptBuilder.build_system_prompt()` to iterate over loaded skills.

---

## Memory Context Injection

Before each call to the LLM, `AgentLoop` retrieves the top-3 memories related to the user's current message:

```python
relevant_memories = self.memory.search(user_input, limit=3)
```

`MemoryStore.search()` runs an FTS5 query against the memories table:

```sql
SELECT content, session_id, importance
FROM memories
WHERE memories MATCH ?
ORDER BY rank
LIMIT ?
```

These memories are displayed in the terminal (via `print_memories()`) so the operator can see what context was retrieved. They are available for inclusion in future prompt extensions.

To extend the prompt with retrieved memories, you can modify `PromptBuilder.build_system_prompt()`:

```python
def build_system_prompt(self, context: str = "", memories: list = None) -> str:
    prompt = base_prompt
    if memories:
        mem_block = "\n".join(f"- {m['content']}" for m in memories)
        prompt += f"\n\nRelevant past context:\n{mem_block}"
    if context:
        prompt += f"\n\nCurrent Context: {context}"
    return prompt
```

---

## Tool Schema Attachment

Tool schemas are NOT part of the system prompt string. They are passed as a separate `tools` argument to `ProviderAdapter.completion()`. This is the Anthropic-native way to register tools.

Each tool schema follows this structure:

```python
{
    "name": "terminal",
    "description": "Execute bash commands in the local system.",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The exact bash command to execute."
            }
        },
        "required": ["command"]
    }
}
```

The `AgentLoop._get_tool_schemas()` method collects schemas from all registered tools:

```python
def _get_tool_schemas(self) -> List[Dict]:
    schemas = []
    for name, fn in self._tool_registry.items():
        if hasattr(fn, "schema"):
            schemas.append(fn.schema)
    return schemas
```

If a tool does not define a `.schema` attribute, `_get_tool_schemas()` falls back to hardcoded schemas for the built-in tools (`terminal`, `file`, `web`). New tools should always define `.schema` on the callable class.

---

## Prompt Caching

When using Anthropic, `pallas_core/prompt_caching.py` injects `cache_control: {"type": "ephemeral"}` breakpoints into the messages array. This instructs Claude to cache the static system prompt and first few tool schemas across turns in the same session, reducing:

- **Latency**: Cached tokens skip re-processing
- **Cost**: Cached input tokens are billed at a reduced rate

The cache breakpoint is placed after the system prompt and after the tool definitions — the two largest static blocks. Dynamic parts (user messages, tool results) are never cached.
