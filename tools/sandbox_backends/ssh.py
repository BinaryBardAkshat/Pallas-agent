"""SSH-based sandbox backend with paramiko (falls back to subprocess ssh/scp)."""
import os
import subprocess
from typing import Optional, Tuple

from . import SandboxBackend


class SSHBackend(SandboxBackend):
    """
    Executes commands on a remote host over SSH.

    Environment variables:
        SSH_HOST     - Remote hostname or IP (required)
        SSH_PORT     - Remote SSH port (default: 22)
        SSH_USER     - Remote username (default: current user)
        SSH_KEY_PATH - Path to private key file (optional; uses SSH agent / default key otherwise)

    Uses paramiko when available for connection pooling; falls back to the
    system ssh/scp binaries otherwise.
    """

    def __init__(self) -> None:
        self.host = os.getenv("SSH_HOST")
        if not self.host:
            raise RuntimeError(
                "SSH_HOST environment variable is required for the SSH sandbox backend."
            )
        self.port = int(os.getenv("SSH_PORT", "22"))
        self.user = os.getenv("SSH_USER", os.getenv("USER", "root"))
        self.key_path = os.getenv("SSH_KEY_PATH")

        # Try to import paramiko for connection pooling.
        self._paramiko_client = None
        try:
            import paramiko  # noqa: F401
            self._use_paramiko = True
            self._connect_paramiko()
        except ImportError:
            self._use_paramiko = False

    # ------------------------------------------------------------------
    # Paramiko helpers
    # ------------------------------------------------------------------

    def _connect_paramiko(self) -> None:
        """Open (or re-open) a persistent paramiko SSH connection."""
        import paramiko

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs: dict = {
            "hostname": self.host,
            "port": self.port,
            "username": self.user,
        }
        if self.key_path:
            connect_kwargs["key_filename"] = self.key_path

        try:
            client.connect(**connect_kwargs)
            self._paramiko_client = client
        except Exception as e:
            raise RuntimeError(
                f"Could not connect to {self.user}@{self.host}:{self.port} via SSH: {e}"
            ) from e

    def _ensure_connection(self) -> None:
        """Reconnect if the paramiko transport has dropped."""
        if self._paramiko_client is None:
            self._connect_paramiko()
            return
        transport = self._paramiko_client.get_transport()
        if transport is None or not transport.is_active():
            self._connect_paramiko()

    def _execute_paramiko(self, command: str, timeout: int) -> Tuple[str, str, int]:
        self._ensure_connection()
        try:
            _, stdout_fh, stderr_fh = self._paramiko_client.exec_command(
                command, timeout=timeout
            )
            exit_code = stdout_fh.channel.recv_exit_status()
            stdout = stdout_fh.read().decode("utf-8", errors="replace")
            stderr = stderr_fh.read().decode("utf-8", errors="replace")
            return stdout, stderr, exit_code
        except Exception as e:
            return "", f"SSH execution error: {e}", 1

    # ------------------------------------------------------------------
    # Subprocess ssh/scp helpers
    # ------------------------------------------------------------------

    def _base_ssh_args(self) -> list:
        args = ["ssh", "-p", str(self.port), "-o", "StrictHostKeyChecking=no"]
        if self.key_path:
            args += ["-i", self.key_path]
        args.append(f"{self.user}@{self.host}")
        return args

    def _execute_subprocess(self, command: str, timeout: int) -> Tuple[str, str, int]:
        args = self._base_ssh_args() + [command]
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", f"SSH command timed out after {timeout} seconds.", 124
        except FileNotFoundError:
            return "", "ssh binary not found. Install OpenSSH client.", 1
        except Exception as e:
            return "", f"SSH subprocess error: {e}", 1

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def execute(self, command: str, timeout: int = 120) -> Tuple[str, str, int]:
        if self._use_paramiko:
            return self._execute_paramiko(command, timeout)
        return self._execute_subprocess(command, timeout)

    def upload_file(self, local_path: str, remote_path: str) -> None:
        if self._use_paramiko:
            self._ensure_connection()
            import paramiko
            with paramiko.SFTPClient.from_transport(
                self._paramiko_client.get_transport()
            ) as sftp:
                sftp.put(local_path, remote_path)
        else:
            dest = f"{self.user}@{self.host}:{remote_path}"
            args = ["scp", "-P", str(self.port), "-o", "StrictHostKeyChecking=no"]
            if self.key_path:
                args += ["-i", self.key_path]
            args += [local_path, dest]
            result = subprocess.run(args, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"SCP upload failed: {result.stderr}")

    def download_file(self, remote_path: str, local_path: str) -> None:
        if self._use_paramiko:
            self._ensure_connection()
            import paramiko
            with paramiko.SFTPClient.from_transport(
                self._paramiko_client.get_transport()
            ) as sftp:
                sftp.get(remote_path, local_path)
        else:
            src = f"{self.user}@{self.host}:{remote_path}"
            args = ["scp", "-P", str(self.port), "-o", "StrictHostKeyChecking=no"]
            if self.key_path:
                args += ["-i", self.key_path]
            args += [src, local_path]
            result = subprocess.run(args, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"SCP download failed: {result.stderr}")

    def __del__(self) -> None:
        if self._paramiko_client:
            try:
                self._paramiko_client.close()
            except Exception:
                pass
