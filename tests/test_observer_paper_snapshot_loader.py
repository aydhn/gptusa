from usa_signal_bot.paper_observer.paper_snapshot_loader import (
    load_observer_read_only_paper_snapshot,
    redact_observer_snapshot_sensitive_fields,
    validate_observer_snapshot_read_only
)

def test_load_observer_read_only_paper_snapshot():
    payload = {"state": "active", "value": 100}
    snapshot = load_observer_read_only_paper_snapshot(payload)
    assert snapshot == payload
    assert snapshot is not payload # deep copy

def test_redact_sensitive_fields():
    snapshot = {"state": "active", "secrets": "my_secret", "tokens": "123"}
    redacted = redact_observer_snapshot_sensitive_fields(snapshot)
    assert redacted["secrets"] == "***REDACTED***"
    assert redacted["tokens"] == "***REDACTED***"
    assert redacted["state"] == "active"

def test_validate_observer_snapshot_read_only():
    snapshot = {"paper_state_committed": True}
    errors = validate_observer_snapshot_read_only(snapshot)
    assert len(errors) == 1
    assert "paper_state_committed=True" in errors[0]
