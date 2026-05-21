from usa_signal_bot.paper_controlled_planning.approval_queue_validator import (
    validate_approval_queue_item_safety, approval_item_has_required_notes, approval_item_blocks_next_stage
)
from usa_signal_bot.paper_controlled_planning.approval_queue import build_final_approval_queue_item
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_validator():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    q = build_final_approval_queue_item(t)
    assert not validate_approval_queue_item_safety(q)
    assert not approval_item_has_required_notes(q)
    assert not approval_item_blocks_next_stage(q)

    q.allows_active_paper = True
    assert len(validate_approval_queue_item_safety(q)) == 1
