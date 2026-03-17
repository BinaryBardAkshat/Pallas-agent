"""Local subprocess-based sandbox backend."""
import subprocess
import os
from typing import Tuple

from . import SandboxBackend


class LocalBackend(SandboxBackend):
    """Executes commands locally using subprocess."""

    def execute(self, command: str, timeout: int = 120) -> Tuple[str, str, int]:
        """
        Execute a shell command locally.

        Returns:
            (stdout, stderr, exit_code)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", f"Command timed out after {timeout} seconds.", 124
        except Exception as e:
            return "", f"Error executing command: {str(e)}", 1
