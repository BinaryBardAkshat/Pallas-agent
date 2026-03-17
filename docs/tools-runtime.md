# Tools Runtime

This document covers how tools are registered, called, approved, and how to add new ones.

---

## Tool Registration

Tools are registered on an `AgentLoop` instance by name. Registration happens in `pallas_core/toolsets.py`:

```python
def register_all(agent, memory_store=None):
    for name, tool in build_default_toolset().items():
        agent.register_tool(name, tool)
    for name, tool in build_memory_toolset(memory_store).items():
        agent.register_tool(name, tool)
```

Internally `AgentLoop.register_tool()` stores the callable in a dict:

```python
def register_tool(self, name: str, fn: Callable):
    self._tool_registry[name] = fn
```

When the LLM returns a tool call, the name is looked up in `_tool_registry` and the function is invoked with the model's `input` dict as keyword arguments:

```python
output = str(tool_fn(**tc["input"]))
```

---

## Schema Format

Every tool must expose an Anthropic-compatible `input_schema`. The schema is a Python dict attached as a `.schema` attribute on the callable object:

```python
class TerminalTool:
    schema = {
        "name": "terminal",
        "description": "Execute a bash command in the local environment.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The exact bash command to run."
                }
            },
            "required": ["command"]
        }
    }

    def __call__(self, command: str) -> str:
        # execution logic
        ...
```

The schema is collected by `AgentLoop._get_tool_schemas()` and sent to the LLM provider as the `tools` parameter. The LLM then generates structured `tool_use` blocks that match this schema.

---

## All Current Tools

| Tool Name | Class | Description |
|---|---|---|
| `terminal` | `TerminalTool` | Execute bash commands via the configured sandbox backend |
| `file` | `FileTool` | Read, write, append, or list files on disk |
| `web` | `WebTool` | Web search queries and URL content fetch |
| `memory` | `MemoryTool` | Store and recall episodic memories from FTS5 DB |
| `code_exec` | `CodeExecutionTool` | Execute Python code in a structured REPL context |
| `skill_manager` | `SkillManagerTool` | List, install, and invoke SKILL.md skill files |
| `session_search` | `SessionSearchTool` | Full-text search across past session messages |
| `todo` | `TodoTool` | Manage a persistent task list (add/complete/list) |
| `vision` | `VisionTool` | Analyze images via Claude Vision or Gemini Vision (optional) |
| `delegate` | `DelegateTool` | Spawn a sub-agent and await its result (optional) |
| `clarify` | `ClarifyTool` | Ask the user a clarifying question mid-task |

---

## SafetyChecker — Blocked Patterns

Before a tool command reaches the sandbox, `tools/safety.py` checks it against a list of 10 danger patterns. Any match causes immediate rejection:

```python
DANGEROUS_PATTERNS = [
    "rm -rf /",       # recursive root deletion
    "sudo rm",        # privileged removal
    "> /dev/sda",     # raw disk overwrite
    "mkfs",           # filesystem formatting
    "dd if=",         # disk duplication/wipe
    ":(){:|:&};:",    # fork bomb
    "chmod -R 777 /", # world-writable root
    "wget http",      # unauthenticated download
    "curl | sh",      # piped shell execution
    "curl | bash",    # piped bash execution
]
```

The check is case-insensitive and substring-based:

```python
def is_dangerous(command: str) -> bool:
    normalized = command.strip().lower()
    return any(p in normalized for p in DANGEROUS_PATTERNS)
```

If a pattern matches, `get_blocked_reason()` returns a human-readable error that is surfaced as the tool result, allowing the model to understand why its command failed and try a safer alternative.

---

## Approval Gates

Every tool call passes through `tools/approval.py` before execution. The `ApprovalGate` is initialized with `enabled=human_in_loop`:

```python
self.approval = ApprovalGate(enabled=human_in_loop)
```

When `enabled=True`, the gate prints the tool name and a preview of its input, then waits for the operator to press `y` or `n`. If declined, the tool call returns `"User declined."` to the model, and the model can choose a different approach.

When `enabled=False` (e.g., `pallas ask` or `pallas start --no-approval`), all tool calls are executed without prompting.

To disable approval for a specific session:

```bash
pallas start --no-approval
```

---

## Sandbox Routing

`TerminalTool` and `CodeExecutionTool` route execution through `tools/sandbox_backends/get_backend()`. The backend is selected by `PALLAS_SANDBOX`:

```bash
PALLAS_SANDBOX=docker pallas start
```

See `docs/sandbox-backends.md` for full backend configuration.

---

## How to Add a New Tool

**Step 1 — Create the tool file**

Create `tools/my_tool.py`:

```python
class MyTool:
    schema = {
        "name": "my_tool",
        "description": "What this tool does in one sentence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "param_one": {
                    "type": "string",
                    "description": "Description of param_one."
                },
                "param_two": {
                    "type": "integer",
                    "description": "Description of param_two.",
                }
            },
            "required": ["param_one"]
        }
    }

    def __call__(self, param_one: str, param_two: int = 0) -> str:
        # Your implementation here.
        result = f"Did something with {param_one}"
        return result
```

**Step 2 — Register in toolsets**

Open `pallas_core/toolsets.py` and add your tool to `build_default_toolset()`:

```python
from tools.my_tool import MyTool

def build_default_toolset() -> Dict[str, Callable]:
    return {
        ...
        "my_tool": MyTool(),
    }
```

**Step 3 — Test it**

```bash
pallas ask "Use my_tool with param_one set to 'hello'"
```

The model will call your tool if the description is clear enough that it recognizes when to use it.

**Step 4 — Add approval bypass if needed**

If your tool is read-only or safe to run without confirmation, you can mark it as auto-approved by extending `ApprovalGate` with an allowlist. By default all tools require confirmation in `human_in_loop` mode.
