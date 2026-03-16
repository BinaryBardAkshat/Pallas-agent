import json
from pathlib import Path
from typing import Dict, Any, Optional
from pallas_constants import CONFIG_PATH

class PallasState:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        return {
            "default_provider": "anthropic",
            "active_session": None,
            "skills_enabled": True
        }

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save()
