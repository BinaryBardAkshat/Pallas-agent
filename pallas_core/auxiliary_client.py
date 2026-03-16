import os
from typing import Any, Dict, List, Optional

from pallas_core.provider_adapter import ProviderAdapter
from .pallas_constants import DEFAULT_MODELS, PROVIDER_ANTHROPIC, PROVIDER_GOOGLE


class AuxiliaryClient:
    def __init__(self, provider: str = PROVIDER_ANTHROPIC):
        self._adapter = ProviderAdapter(provider)

    def quick_completion(self, prompt: str, max_tokens: int = 1024) -> str:
        result = self._adapter.completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return result.get("content", "")

    def classify(self, text: str, categories: List[str]) -> str:
        prompt = (
            f"Classify the following text into exactly one of these categories: {', '.join(categories)}.\n"
            f"Text: {text}\n"
            f"Respond with just the category name."
        )
        return self.quick_completion(prompt, max_tokens=50).strip()

    def summarize(self, text: str, max_length: int = 200) -> str:
        prompt = (
            f"Summarize the following in under {max_length} characters. Be concise and factual.\n\n{text}"
        )
        return self.quick_completion(prompt, max_tokens=256)

    def extract_keywords(self, text: str, count: int = 5) -> List[str]:
        prompt = (
            f"Extract {count} keywords from this text. "
            f"Return them as a comma-separated list, nothing else.\n\n{text}"
        )
        result = self.quick_completion(prompt, max_tokens=100)
        return [k.strip() for k in result.split(",") if k.strip()]
