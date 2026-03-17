"""Docker-based sandbox backend."""
import os
import shutil
import subprocess
from typing import Tuple

from . import SandboxBackend


class DockerBackend(SandboxBackend):
    """
    Executes commands inside a Docker container via the docker CLI.

    Environment variables:
        DOCKER_IMAGE     - Docker image to use (default: python:3.11-slim)
        DOCKER_WORKSPACE - Host directory mounted into /workspace (default: cwd)
    """

    def __init__(self) -> None:
        if not shutil.which("docker"):
            raise RuntimeError(
                "Docker CLI not found. Install Docker and ensure 'docker' is on your PATH."
            )
        self.image = os.getenv("DOCKER_IMAGE", "python:3.11-slim")
        self.workspace = os.getenv("DOCKER_WORKSPACE", os.getcwd())

    def _run(self, args: list, timeout: int) -> Tuple[str, str, int]:
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", f"Docker command timed out after {timeout} seconds.", 124
        except Exception as e:
            return "", f"Docker error: {str(e)}", 1

    def execute(self, command: str, timeout: int = 120) -> Tuple[str, str, int]:
        """
        Run a shell command inside a fresh Docker container.

        The host workspace is bind-mounted at /workspace and set as the
        working directory inside the container.
        """
        args = [
            "docker", "run", "--rm",
            "-v", f"{self.workspace}:/workspace",
            "-w", "/workspace",
            self.image,
            "sh", "-c", command,
        ]
        return self._run(args, timeout)

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Copy a file from the host into a running container is not applicable
        for --rm containers. This method copies the file into the workspace
        directory which is shared via volume mount.
        """
        dest = os.path.join(self.workspace, remote_path.lstrip("/workspace").lstrip("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        import shutil as _shutil
        _shutil.copy2(local_path, dest)

    def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Retrieve a file that was written into the shared workspace volume.
        """
        src = os.path.join(self.workspace, remote_path.lstrip("/workspace").lstrip("/"))
        import shutil as _shutil
        _shutil.copy2(src, local_path)
