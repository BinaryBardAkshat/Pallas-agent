import re
from typing import Dict, List, Optional


_SECRET_PATTERNS = [
    re.compile(r"(sk-[a-zA-Z0-9]{20,})", re.IGNORECASE),
    re.compile(r"(AKIA[0-9A-Z]{16})", re.IGNORECASE),
    re.compile(r"(['\"]?(?:api[-_]?key|secret|token|password|passwd)['\"]?\s*[:=]\s*['\"]?)([a-zA-Z0-9_\-\.]{8,})", re.IGNORECASE),
    re.compile(r"(ghp_[a-zA-Z0-9]{36})", re.IGNORECASE),
    re.compile(r"(ghs_[a-zA-Z0-9]{36})", re.IGNORECASE),
]

PLACEHOLDER = "[REDACTED]"


def redact(text: str) -> str:
    for pattern in _SECRET_PATTERNS:
        if pattern.groups == 1:
            text = pattern.sub(PLACEHOLDER, text)
        else:
            text = pattern.sub(lambda m: m.group(1) + PLACEHOLDER, text)
    return text


def redact_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{"role": m["role"], "content": redact(m["content"])} for m in messages]
