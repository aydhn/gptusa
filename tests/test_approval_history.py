from usa_signal_bot.paper_controlled_planning.approval_history import build_approval_history, latest_approval_decision
from usa_signal_bot.paper_controlled_planning.approval_queue import build_final_approval_queue_item, mark_approval_queue_item_for_next_non_executing_stage
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket
from usa_signal_bot.core.enums import ApprovalQueueDecision

def test_history():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    q = build_final_approval_queue_item(t)
    hist = build_approval_history([q])
    assert len(hist) == 1
    assert latest_approval_decision([q]) == ApprovalQueueDecision.INCONCLUSIVE

    q2 = mark_approval_queue_item_for_next_non_executing_stage(q)
    assert latest_approval_decision([q2]) == ApprovalQueueDecision.APPROVE_FOR_NEXT_NON_EXECUTING_STAGE
