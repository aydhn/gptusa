from usa_signal_bot.paper_controlled_planning.approval_queue import (
    build_final_approval_queue_item, update_approval_queue_item_notes,
    mark_approval_queue_item_for_next_non_executing_stage, reject_approval_queue_item, block_approval_queue_item
)
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket
from usa_signal_bot.core.enums import ApprovalQueueItemStatus, ApprovalQueueDecision

def test_approval_queue():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    q = build_final_approval_queue_item(t)
    assert q.status == ApprovalQueueItemStatus.QUEUED
    assert q.decision == ApprovalQueueDecision.INCONCLUSIVE

    q = update_approval_queue_item_notes(q, "LGTM")
    assert q.status == ApprovalQueueItemStatus.REVIEWED_WITH_NOTES

    q = mark_approval_queue_item_for_next_non_executing_stage(q)
    assert q.status == ApprovalQueueItemStatus.APPROVED_FOR_NEXT_NON_EXECUTING_STAGE
    assert q.decision == ApprovalQueueDecision.APPROVE_FOR_NEXT_NON_EXECUTING_STAGE
