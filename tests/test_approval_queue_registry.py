from usa_signal_bot.paper_controlled_planning.approval_queue_registry import (
    register_approval_queue_item, find_approval_item_by_id, latest_approval_item_for_candidate
)
from usa_signal_bot.paper_controlled_planning.approval_queue import build_final_approval_queue_item
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_registry():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    q = build_final_approval_queue_item(t)
    reg = register_approval_queue_item(q)
    assert len(reg) == 1
    assert find_approval_item_by_id(reg, q.queue_item_id) == q
    assert latest_approval_item_for_candidate(reg, "c1") == q
