from typing import List

DANGEROUS_PATTERNS = [
    "rm -rf /",
    "sudo rm",
    "> /dev/sda",
    "mkfs",
    "dd if=",
    ":(){:|:&};:",
    "chmod -R 777 /",
    "wget http",
    "curl | sh",
    "curl | bash",
]


def is_dangerous(command: str) -> bool:
    normalized = command.strip().lower()
    return any(p in normalized for p in DANGEROUS_PATTERNS)


def get_blocked_reason(command: str) -> str:
    for p in DANGEROUS_PATTERNS:
        if p in command.strip().lower():
            return f"Blocked: dangerous pattern '{p}' detected."
    return ""
