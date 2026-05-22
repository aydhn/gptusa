import pytest
from usa_signal_bot.paper_pre_rehearsal.paper_runtime_adapter import build_read_only_paper_snapshot_for_pre_paper_rehearsal

def test_runtime():
    snap = build_read_only_paper_snapshot_for_pre_paper_rehearsal({"data": 1})
    assert not snap["paper_state_committed"]
