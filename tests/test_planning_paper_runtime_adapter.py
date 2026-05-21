from usa_signal_bot.paper_controlled_planning.paper_runtime_adapter import build_read_only_paper_runtime_snapshot_for_planning, validate_paper_runtime_not_mutated_by_planning

def test_runtime_adapter():
    snap = build_read_only_paper_runtime_snapshot_for_planning({"some": "val"})
    assert snap["read_only"]
    assert not snap["paper_state_committed"]

    errs = validate_paper_runtime_not_mutated_by_planning({}, {"paper_state_committed": True})
    assert len(errs) == 1
