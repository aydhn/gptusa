from usa_signal_bot.paper_controlled_planning.adjacent_rehearsal_context import (
    build_paper_adjacent_rehearsal_context, build_mock_paper_adjacent_rehearsal_context,
    validate_adjacent_context_safety
)
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_adjacent_context():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    ctx = build_paper_adjacent_rehearsal_context(t)
    assert ctx.candidate_id == "c1"
    assert ctx.allow_active_paper is False
    assert not validate_adjacent_context_safety(ctx)

    ctx.allow_active_paper = True
    assert len(validate_adjacent_context_safety(ctx)) == 1
