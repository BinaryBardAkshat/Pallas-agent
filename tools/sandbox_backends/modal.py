"""Modal.com cloud sandbox backend."""
import os
from typing import Tuple

from . import SandboxBackend


class ModalBackend(SandboxBackend):
    """
    Executes commands on Modal.com serverless infrastructure.

    Environment variables:
        MODAL_TOKEN_ID     - Modal API token ID
        MODAL_TOKEN_SECRET - Modal API token secret

    Requires the 'modal' Python package:
        pip install modal
    """

    def __init__(self) -> None:
        self.token_id = os.getenv("MODAL_TOKEN_ID")
        self.token_secret = os.getenv("MODAL_TOKEN_SECRET")

        try:
            import modal  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "The 'modal' package is required for the Modal sandbox backend. "
                "Install it with: pip install modal"
            ) from exc

        # Configure credentials if provided via env vars (Modal also reads
        # ~/.modal.toml or MODAL_TOKEN_ID/MODAL_TOKEN_SECRET automatically).
        if self.token_id and self.token_secret:
            import modal
            modal.config._token_id = self.token_id
            modal.config._token_secret = self.token_secret

    def execute(self, command: str, timeout: int = 120) -> Tuple[str, str, int]:
        """
        Run a shell command in an ephemeral Modal sandbox.

        Returns:
            (stdout, stderr, exit_code)
        """
        import modal

        app = modal.App.lookup("pallas-sandbox", create_if_missing=True)

        image = modal.Image.debian_slim().pip_install("bash")

        @app.function(image=image, timeout=timeout)
        def _run(cmd: str) -> dict:
            import subprocess as _sp
            result = _sp.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        try:
            with modal.runner.deploy_stub(app):
                output = _run.remote(command)
            return output["stdout"], output["stderr"], output["returncode"]
        except modal.exception.TimeoutError:
            return "", f"Modal command timed out after {timeout} seconds.", 124
        except Exception as e:
            return "", f"Modal execution error: {str(e)}", 1
