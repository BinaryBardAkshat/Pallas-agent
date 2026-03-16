from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ModelInfo:
    provider: str
    model_id: str
    context_window: int
    max_output_tokens: int
    supports_tools: bool = True
    supports_vision: bool = False
    cost_per_1m_input: float = 0.0
    cost_per_1m_output: float = 0.0


KNOWN_MODELS: Dict[str, ModelInfo] = {
    "claude-sonnet-4-6": ModelInfo(
        provider="anthropic",
        model_id="claude-sonnet-4-6",
        context_window=200_000,
        max_output_tokens=8192,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=3.0,
        cost_per_1m_output=15.0,
    ),
    "claude-opus-4-1": ModelInfo(
        provider="anthropic",
        model_id="claude-opus-4-1",
        context_window=200_000,
        max_output_tokens=8192,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=15.0,
        cost_per_1m_output=75.0,
    ),
    "claude-3-5-haiku-latest": ModelInfo(
        provider="anthropic",
        model_id="claude-3-5-haiku-latest",
        context_window=200_000,
        max_output_tokens=4096,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=0.25,
        cost_per_1m_output=1.25,
    ),
    "gemini-2.5-pro": ModelInfo(
        provider="google",
        model_id="gemini-2.5-pro",
        context_window=1_000_000,
        max_output_tokens=8192,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=3.5,
        cost_per_1m_output=10.5,
    ),
    "gemini-2.5-flash": ModelInfo(
        provider="google",
        model_id="gemini-2.5-flash",
        context_window=1_000_000,
        max_output_tokens=8192,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=0.075,
        cost_per_1m_output=0.30,
    ),
    "gemini-2.5-flash-lite": ModelInfo(
        provider="google",
        model_id="gemini-2.5-flash-lite",
        context_window=1_000_000,
        max_output_tokens=8192,
        supports_tools=False,
        supports_vision=True,
        cost_per_1m_input=0.02,
        cost_per_1m_output=0.10,
    ),
    "gpt-5.4": ModelInfo(
        provider="openai",
        model_id="gpt-5.4",
        context_window=128_000,
        max_output_tokens=8192,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=5.0,
        cost_per_1m_output=15.0,
    ),
    "gpt-5.4-pro": ModelInfo(
        provider="openai",
        model_id="gpt-5.4-pro",
        context_window=128_000,
        max_output_tokens=8192,
        supports_tools=True,
        supports_vision=True,
        cost_per_1m_input=30.0,
        cost_per_1m_output=60.0,
    ),
    "qwen3.5:27b": ModelInfo(
        provider="ollama",
        model_id="qwen3.5:27b",
        context_window=32_768,
        max_output_tokens=4096,
        supports_tools=True,
        supports_vision=False,
        cost_per_1m_input=0.0,
        cost_per_1m_output=0.0,
    ),
    "qwen3:14b": ModelInfo(
        provider="ollama",
        model_id="qwen3:14b",
        context_window=32_768,
        max_output_tokens=4096,
        supports_tools=True,
        supports_vision=False,
        cost_per_1m_input=0.0,
        cost_per_1m_output=0.0,
    ),
}


def get_model_info(model_id: str) -> Optional[ModelInfo]:
    return KNOWN_MODELS.get(model_id)


def suggest_model(task_type: str) -> str:
    routing = {
        "coding": "claude-sonnet-4-6",
        "research": "gemini-2.5-pro",
        "quick": "gemini-2.5-flash",
        "vision": "claude-sonnet-4-6",
        "heavy": "gpt-5.4-pro",
        "local": "qwen3.5:27b",
    }
    return routing.get(task_type, "claude-sonnet-4-6")
