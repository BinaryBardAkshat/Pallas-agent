import threading
from typing import Any


class InterruptManager:
    """Manage graceful interruptions of the agent loop."""

    def __init__(self):
        self._stop_flag = threading.Event()

    def request_stop(self):
        self._stop_flag.set()

    def is_stopped(self) -> bool:
        return self._stop_flag.is_set()

    def reset(self):
        self._stop_flag.clear()

    def register_with_loop(self, agent_loop: Any):
        """Monkey-patch agent_loop.run to check _stop_flag and reset on each call."""
        original_run = agent_loop.run

        def wrapped_run(user_input: str) -> str:
            self.reset()
            return original_run(user_input)

        agent_loop.run = wrapped_run
