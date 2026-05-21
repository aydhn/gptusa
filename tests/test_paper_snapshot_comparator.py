from usa_signal_bot.paper_controlled_planning.paper_snapshot_comparator import (
    build_read_only_paper_snapshot_for_planning, compare_candidate_to_read_only_paper_snapshot,
    validate_paper_snapshot_not_mutated
)
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_paper_snapshot():
    snap = build_read_only_paper_snapshot_for_planning({"some_data": 123})
    assert snap["read_only"] is True
    assert snap["paper_state_committed"] is False

    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    comp = compare_candidate_to_read_only_paper_snapshot(t, snap)
    assert comp["is_read_only"] is True

    errs = validate_paper_snapshot_not_mutated({}, {"paper_state_committed": True})
    assert len(errs) == 1
