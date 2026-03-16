import subprocess
import sys
import textwrap
from typing import Any, Optional


class CodeExecutionTool:
    name = "code_exec"
    description = "Execute a Python code snippet in a subprocess and return its stdout."

    def __call__(self, code: str, timeout: int = 30) -> str:
        try:
            result = subprocess.run(
                [sys.executable, "-c", textwrap.dedent(code)],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = result.stdout
            if result.returncode != 0:
                output += f"\n[Error]\n{result.stderr}"
            return output.strip() or "(no output)"
        except subprocess.TimeoutExpired:
            return "Code execution timed out."
        except Exception as e:
            return f"Execution error: {e}"
