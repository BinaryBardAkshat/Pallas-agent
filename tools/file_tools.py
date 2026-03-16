import subprocess
import os
from typing import Dict, Any

class TerminalTool:
    def __init__(self, sandbox: str = "local"):
        self.sandbox = sandbox

    def __call__(self, command: str) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                timeout=120
            )
            output = result.stdout or ""
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            return output if output.strip() else "Process completed successfully with no output."
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after 120 seconds."
        except Exception as e:
            return f"Error executing command: {str(e)}"

class FileTool:
    def __call__(self, action: str, path: str, content: str = None) -> str:
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
