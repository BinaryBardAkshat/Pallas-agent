from datetime import datetime, timezone, timedelta
from typing import Optional


def utcnow() -> datetime:
    """Return the current time in UTC with timezone info."""
    return datetime.now(timezone.utc)


def timestamp() -> str:
    """Return an ISO-8601 formatted timestamp string in UTC."""
    return utcnow().isoformat()


def human_elapsed(since: datetime) -> str:
    """Return a human-readable elapsed duration (e.g. '5m', '2h', '30s')."""
    now = utcnow()
    diff = now - since
    total_seconds = int(diff.total_seconds())

    if total_seconds < 0:
        return "now"

    if total_seconds < 60:
        return f"{total_seconds}s"

    minutes = total_seconds // 60
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    if hours < 24:
        return f"{hours}h"

    days = hours // 24
    if days < 7:
        return f"{days}d"
    
    weeks = days // 7
    return f"{weeks}w"
