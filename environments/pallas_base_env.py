import subprocess
import os
import shlex
from typing import Optional


class LocalEnv:
    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = working_dir or os.getcwd()
        self.env_vars = dict(os.environ)

    def run(self, command: str, timeout: int = 30) -> str:
        result = subprocess.run(
            shlex.split(command),
            cwd=self.working_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=self.env_vars,
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        return output.strip()

    def set_env(self, key: str, value: str):
        self.env_vars[key] = value

    def change_dir(self, path: str):
        self.working_dir = str(os.path.expanduser(path))
