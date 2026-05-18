import pytest
from usa_signal_bot.research_execution.config_snapshot import stable_config_hash, redact_config_secrets, build_candidate_config_snapshot

def test_stable_config_hash():
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "a": 1}
    assert stable_config_hash(d1) == stable_config_hash(d2)

def test_redact_config_secrets():
    payload = {
        "normal": "value",
        "nested": {
            "some_token": "secret123",
            "db_password": "pass"
        }
    }
    redacted = redact_config_secrets(payload)
    assert redacted["nested"]["some_token"] == "[REDACTED]"
