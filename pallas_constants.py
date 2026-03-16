import os
from pathlib import Path

PROJECT_NAME = "Pallas"
VERSION = "0.1.0"

HOME_DIR = Path.home() / ".pallas"
CONFIG_PATH = HOME_DIR / "config.json"
DATA_DIR = HOME_DIR / "data"
SKILLS_DIR = HOME_DIR / "skills"
LOGS_DIR = HOME_DIR / "logs"

DEFAULT_MODEL_CLAUDE = "claude-3-5-sonnet-20240620"
DEFAULT_MODEL_GEMINI = "gemini-1.5-pro"

# Ensure directories exist
for directory in [HOME_DIR, DATA_DIR, SKILLS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
