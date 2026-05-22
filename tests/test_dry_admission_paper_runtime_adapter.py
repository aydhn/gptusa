from usa_signal_bot.paper_dry_admission.paper_runtime_adapter import build_read_only_paper_snapshot_for_dry_admission

def test_paper_runtime_adapter():
    snap = build_read_only_paper_snapshot_for_dry_admission({"some_key": "val"})
    assert snap["read_only"] is True
    assert snap["paper_state_committed"] is False
