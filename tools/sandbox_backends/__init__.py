"""Sandbox execution backends for Pallas terminal tool."""
import os
from abc import ABC, abstractmethod
from typing import Tuple


class SandboxBackend(ABC):
    """Abstract base for sandbox execution backends."""

    @abstractmethod
    def execute(self, command: str, timeout: int = 120) -> Tuple[str, str, int]:
        """Execute command. Returns (stdout, stderr, exit_code)."""
        pass

    def upload_file(self, local_path: str, remote_path: str) -> None:
        pass

    def download_file(self, remote_path: str, local_path: str) -> None:
        pass


def get_backend() -> SandboxBackend:
    """Return configured backend based on PALLAS_SANDBOX env var."""
    backend_name = os.getenv("PALLAS_SANDBOX", "local").lower()
    if backend_name == "docker":
        from .docker import DockerBackend
        return DockerBackend()
    elif backend_name == "ssh":
        from .ssh import SSHBackend
        return SSHBackend()
    elif backend_name == "modal":
        from .modal import ModalBackend
        return ModalBackend()
    else:
        from .local import LocalBackend
        return LocalBackend()
