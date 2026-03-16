from typing import Any, Dict, List, Optional

from pallas_constants import DEFAULT_MODELS, PROVIDER_ANTHROPIC


class ContextCompressor:
    def __init__(self, max_tokens: int = 100_000):
        self.max_tokens = max_tokens

    def compress(self, messages: List[Dict[str, str]], token_budget: int = 0) -> List[Dict[str, str]]:
        budget = token_budget or self.max_tokens
        total = sum(self._estimate_tokens(m["content"]) for m in messages)

        if total <= budget:
            return messages

        compressed = []
        running = 0

        for m in reversed(messages):
            est = self._estimate_tokens(m["content"])
            if running + est > budget:
                break
            compressed.insert(0, m)
            running += est

        if not compressed and messages:
            last = messages[-1]
            truncated_content = last["content"][:budget * 3]
            compressed = [{"role": last["role"], "content": truncated_content}]

        return compressed

    def summarize_prefix(self, messages: List[Dict[str, str]], keep_last: int = 10) -> List[Dict[str, str]]:
        if len(messages) <= keep_last:
            return messages

        prefix = messages[:-keep_last]
        suffix = messages[-keep_last:]

        summary_parts = []
        for m in prefix:
            summary_parts.append(f"[{m['role']}] {m['content'][:100]}")

        summary = "Previous conversation summary:\n" + "\n".join(summary_parts)
        return [{"role": "user", "content": summary}] + suffix

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return len(text) // 4
