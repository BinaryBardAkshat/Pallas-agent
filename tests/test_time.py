import pytest
from pallas_core.pallas_time import utcnow, timestamp, human_elapsed
import time
from datetime import datetime, timezone, timedelta


def test_utcnow_is_utc():
    dt = utcnow()
    assert dt.tzinfo is not None


def test_timestamp_is_string():
    ts = timestamp()
    assert isinstance(ts, str)
    assert "T" in ts


def test_human_elapsed_seconds():
    since = utcnow() - timedelta(seconds=30)
    result = human_elapsed(since)
    assert "s" in result


def test_human_elapsed_minutes():
    since = utcnow() - timedelta(minutes=5)
    result = human_elapsed(since)
    assert "m" in result
