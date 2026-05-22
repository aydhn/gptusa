import pytest
from usa_signal_bot.paper_pre_rehearsal.paper_baseline_loader import load_read_only_paper_baseline_for_pre_rehearsal

def test_load_baseline():
    payload = {"api_key": "secret", "data": "val"}
    baseline = load_read_only_paper_baseline_for_pre_rehearsal(payload)
    assert baseline["api_key"] == "[REDACTED]"
    assert baseline["data"] == "val"
    assert not baseline["paper_state_committed"]
