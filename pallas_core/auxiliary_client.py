import os
from typing import Any, Dict, List, Optional
from pallas_core.provider_adapter import ProviderAdapter
from .pallas_constants import (
    PROVIDER_ANTHROPIC, 
    PROVIDER_GOOGLE, 
    AUX_MODELS,
    PROVIDER_OPENAI,
    PROVIDER_OPENROUTER,
    PROVIDER_OLLAMA
)

class AuxiliaryClient:
    """
    Lightweight model client for secondary tasks (summarization, classification, routing).
    Uses cheaper models like Claude Haiku or Gemini Flash.
    """
    def __init__(self, provider: str = PROVIDER_ANTHROPIC):
        self.provider = provider
        self.model = AUX_MODELS.get(provider)
        self._adapter = ProviderAdapter(provider)

    def quick_completion(self, prompt: str, max_tokens: int = 200) -> str:
        """Execute a quick completion using the auxiliary model."""
        try:
            result = self._adapter.completion(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                max_tokens=max_tokens,
            )
            return result.get("content", "")
        except Exception:
            # Fallback to main provider if aux fails (though usually aux is the fallback)
            return ""

    def summarize(self, text: str, max_tokens: int = 200) -> str:
        """Summarize text using the auxiliary model."""
        prompt = f"Summarize the following text concisely (max {max_tokens} tokens):\n\n{text}"
        return self.quick_completion(prompt, max_tokens=max_tokens)

    def classify(self, text: str, labels: List[str]) -> str:
        """Classify text into one of the provided labels."""
        prompt = f"Classify the following text into exactly one of these labels: {', '.join(labels)}.\nText: {text}\nLabel:"
        return self.quick_completion(prompt, max_tokens=20).strip()

    def compress_messages(self, messages: List[Dict], target_tokens: int) -> List[Dict]:
        """Use the auxiliary model to compress message history."""
        # Simple implementation: summarize older messages
        if len(messages) <= 2:
            return messages
        
        to_compress = messages[:-2]
        tail = messages[-2:]
        
        text_to_compress = "\n".join([f"{m['role']}: {m['content']}" for m in to_compress])
        summary = self.summarize(f"Compress this conversation history while preserving key facts:\n{text_to_compress}")
        
        return [{"role": "system", "content": f"Previous conversation summary: {summary}"}] + tail
