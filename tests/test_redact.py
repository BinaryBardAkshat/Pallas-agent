import pytest
from pallas_core.redact import redact


def test_redact_anthropic_key():
    text = "my key is sk-ant-api03-abcdefghijklmnopqrstuvwxyz12345"
    assert "[REDACTED]" in redact(text)


def test_redact_github_token():
    text = "token: ghp_abcdefghijklmnopqrstuvwxyz123456789"
    assert "[REDACTED]" in redact(text)


def test_no_redact_normal_text():
    text = "Hello, this is a normal sentence with no secrets."
    assert redact(text) == text
