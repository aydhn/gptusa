import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.paper_runtime_adapter import build_read_only_paper_snapshot_for_handoff_freeze

def test_build_read_only_paper_snapshot_for_handoff_freeze():
    payload = {"state": "active"}
    snapshot = build_read_only_paper_snapshot_for_handoff_freeze(payload)
    assert snapshot["state"] == "active"
    assert snapshot["read_only_snapshot"] is True
    assert snapshot["paper_state_committed"] is False
