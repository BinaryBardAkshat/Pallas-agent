import os
from typing import Optional
from dotenv import load_dotenv
from pallas_constants import PROVIDER_ANTHROPIC


def get_runtime_provider() -> str:
    load_dotenv()
    return os.getenv("PALLAS_PROVIDER", PROVIDER_ANTHROPIC)


def get_runtime_model() -> Optional[str]:
    load_dotenv()
    return os.getenv("PALLAS_MODEL") or None


def is_approval_disabled() -> bool:
    load_dotenv()
    return os.getenv("PALLAS_NO_APPROVAL", "").lower() in ("1", "true", "yes")
