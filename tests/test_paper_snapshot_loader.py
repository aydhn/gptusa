import pytest
from usa_signal_bot.paper_dry_run_bridge.paper_snapshot_loader import (
    load_read_only_paper_snapshot,
    redact_paper_snapshot_sensitive_fields,
    paper_snapshot_hash,
    validate_paper_snapshot_read_only,
    paper_snapshot_loader_summary,
    paper_snapshot_loader_to_text
)

def test_paper_snapshot_loader():
    payload = {
        "snapshot_id": "snap_123",
        "paper_state_committed": True,
        "api_key": "secret123"
    }

    snapshot = load_read_only_paper_snapshot(payload)
    assert snapshot["paper_state_committed"] is False

    redacted = redact_paper_snapshot_sensitive_fields(snapshot)
    assert redacted["api_key"] == "[REDACTED]"

    assert len(validate_paper_snapshot_read_only(redacted)) == 0

    h = paper_snapshot_hash(redacted)
    assert h is not None

    summary = paper_snapshot_loader_summary(redacted)
    assert summary["read_only"] is True

    assert "Read-Only: True" in paper_snapshot_loader_to_text(redacted)
