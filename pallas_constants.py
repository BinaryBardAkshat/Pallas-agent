import os
from pathlib import Path

PROJECT_NAME = "Pallas"
VERSION = "0.1.0"
VINKURA_BRAND = "Vinkura AI"

HOME_DIR = Path.home() / ".pallas"
CONFIG_PATH = HOME_DIR / "config.json"
DATA_DIR = HOME_DIR / "data"
SKILLS_DIR = HOME_DIR / "skills"
LOGS_DIR = HOME_DIR / "logs"
DB_PATH = DATA_DIR / "pallas.db"
MEMORY_DB_PATH = DATA_DIR / "memory.db"
SESSIONS_DB_PATH = DATA_DIR / "sessions.db"

PROVIDER_ANTHROPIC = "anthropic"
PROVIDER_GOOGLE = "google"
PROVIDER_OPENAI = "openai"
PROVIDER_OPENROUTER = "openrouter"
PROVIDER_OLLAMA = "ollama"

DEFAULT_MODEL_ANTHROPIC = "claude-sonnet-4-6"
DEFAULT_MODEL_GOOGLE = "gemini-2.5-pro"
DEFAULT_MODEL_OPENAI = "gpt-5.4"
DEFAULT_MODEL_OPENROUTER = "anthropic/claude-sonnet-4.6"
DEFAULT_MODEL_OLLAMA = "qwen3.5:27b"

DEFAULT_MODELS = {
    PROVIDER_ANTHROPIC: DEFAULT_MODEL_ANTHROPIC,
    PROVIDER_GOOGLE: DEFAULT_MODEL_GOOGLE,
    PROVIDER_OPENAI: DEFAULT_MODEL_OPENAI,
    PROVIDER_OPENROUTER: DEFAULT_MODEL_OPENROUTER,
    PROVIDER_OLLAMA: DEFAULT_MODEL_OLLAMA,
}

CODING_MODEL_ANTHROPIC = "claude-sonnet-4-6"
RESEARCH_MODEL_GOOGLE = "gemini-2.5-pro"
GENERAL_MODEL_ANTHROPIC = "claude-sonnet-4-6"
HEAVY_REASONING_OPENAI = "gpt-5.4-pro"

TASK_TYPE_CODING = "coding"
TASK_TYPE_RESEARCH = "research"
TASK_TYPE_GENERAL = "general"

PROVIDER_ROUTING = {
    TASK_TYPE_CODING: PROVIDER_ANTHROPIC,
    TASK_TYPE_RESEARCH: PROVIDER_GOOGLE,
    TASK_TYPE_GENERAL: PROVIDER_ANTHROPIC,
}

TASK_MODEL_PREFERENCES = {
    TASK_TYPE_CODING: {
        PROVIDER_ANTHROPIC: CODING_MODEL_ANTHROPIC,
        PROVIDER_OPENAI: "gpt-5.4",
        PROVIDER_OPENROUTER: "anthropic/claude-sonnet-4.6",
        PROVIDER_OLLAMA: "qwen3.5:27b",
    },
    TASK_TYPE_RESEARCH: {
        PROVIDER_GOOGLE: RESEARCH_MODEL_GOOGLE,
        PROVIDER_OPENAI: "gpt-5.4",
        PROVIDER_OPENROUTER: "google/gemini-2.5-pro",
        PROVIDER_OLLAMA: "qwen3.5:27b",
    },
    TASK_TYPE_GENERAL: {
        PROVIDER_ANTHROPIC: GENERAL_MODEL_ANTHROPIC,
        PROVIDER_GOOGLE: "gemini-2.5-flash",
        PROVIDER_OPENAI: "gpt-5.4",
        PROVIDER_OPENROUTER: "anthropic/claude-sonnet-4.6",
        PROVIDER_OLLAMA: "qwen3:14b",
    },
}

PROVIDER_ENDPOINTS = {
    PROVIDER_ANTHROPIC: "https://api.anthropic.com/v1/messages",
    PROVIDER_GOOGLE: "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    PROVIDER_OPENAI: "https://api.openai.com/v1/responses",
    PROVIDER_OPENROUTER: "https://openrouter.ai/api/v1/chat/completions",
    PROVIDER_OLLAMA: "http://localhost:11434/api/chat",
}

for directory in [HOME_DIR, DATA_DIR, SKILLS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
