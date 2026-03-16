from typing import Optional


class ApprovalGate:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def request(self, tool_name: str, description: str = "") -> bool:
        if not self.enabled:
            return True

        prompt = f"\n  Approve tool '{tool_name}'"
        if description:
            prompt += f" ({description})"
        prompt += "? [y/N] "

        try:
            answer = input(prompt).strip().lower()
            return answer in ("y", "yes")
        except (EOFError, KeyboardInterrupt):
            return False
