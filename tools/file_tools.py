import os
from typing import Dict, Any

from .sandbox_backends import get_backend


class TerminalTool:
    schema = {
        "name": "terminal",
        "description": (
            "Execute any bash shell command on the user's local machine. "
            "Use for: running scripts, listing files, installing packages, git, compiling code, reading program output. "
            "You have full shell access. Always pass the 'command' parameter."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run, e.g. 'ls -la', 'python script.py', 'pip install requests'",
                }
            },
            "required": ["command"],
        },
    }

    def __init__(self, sandbox: str = "local"):
        self.sandbox = sandbox
        self._backend = get_backend()

    def __call__(self, command: str, timeout: int = 120) -> str:
        try:
            stdout, stderr, exit_code = self._backend.execute(command, timeout=timeout)
            output = stdout or ""
            if stderr:
                output += f"\nSTDERR:\n{stderr}"
            if exit_code not in (0, None) and not output.strip():
                output = f"Process exited with code {exit_code} and no output."
            return output if output.strip() else "Process completed successfully with no output."
        except Exception as e:
            return f"Error executing command: {str(e)}"

class FileTool:
    schema = {
        "name": "file",
        "description": "Read, write, append, or list files and directories on the local filesystem.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["read", "write", "append", "list"],
                    "description": "Operation: 'read' to get file content, 'write' to create/overwrite, 'append' to add to end, 'list' to show directory contents",
                },
                "path": {
                    "type": "string",
                    "description": "File or directory path, e.g. '/tmp/file.txt' or '~/Documents/note.md'",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write or append. Only required for 'write' and 'append' actions.",
                },
            },
            "required": ["action", "path"],
        },
    }

    def __call__(self, action: str = None, path: str = None, content: str = None, **kwargs) -> str:
        # ── Normalise aliases before any validation ──────────────────────────
        _SHORT = {"w": "write", "r": "read", "a": "append"}

        # 1. Resolve action aliases
        if action in _SHORT:
            action = _SHORT[action]
        if not action:
            raw_mode = kwargs.get("mode", "")
            action = _SHORT.get(raw_mode, raw_mode) or None

        # 2. Resolve path + action from boolean/path-value kwargs
        #    e.g. write=True, write='/tmp/file', read='/tmp/file'
        if not action or not path:
            for kw, act in (("write", "write"), ("read", "read"), ("append", "append")):
                val = kwargs.get(kw)
                if val is None:
                    continue
                if not action:
                    action = act
                if not path and isinstance(val, str) and len(val) > 1 and val not in ("True", "False", "1", "0"):
                    path = val
                break

        # 3. Other path aliases
        if not path:
            path = (kwargs.get("filename") or kwargs.get("name") or
                    kwargs.get("file_path") or kwargs.get("filepath") or "")

        if not action:
            action = "read"
        if not path:
            return "Error: 'path' parameter is required. Use action='write', path='...', content='...'"
        try:
            expanded_path = os.path.expanduser(path)
            if action == "read":
                with open(expanded_path, "r") as f:
                    return f.read()
            elif action == "write":
                with open(expanded_path, "w") as f:
                    f.write(content or "")
                return f"Successfully wrote to {path}"
            elif action == "append":
                with open(expanded_path, "a") as f:
                    f.write(content or "")
                return f"Successfully appended to {path}"
            elif action == "list":
                if os.path.isdir(expanded_path):
                    return "\n".join(os.listdir(expanded_path))
                return f"Error: {path} is not a directory."
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as e:
            return f"Error performing {action} on {path}: {str(e)}"
