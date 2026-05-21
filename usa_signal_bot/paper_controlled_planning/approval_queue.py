from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    FinalHumanApprovalQueueItem,
    ControlledPlanningTicket,
    PaperAdjacentRehearsalRun,
    create_final_approval_queue_item_id,
    _now_str
)
from usa_signal_bot.core.enums import (
    ApprovalQueueItemStatus,
    ApprovalQueueDecision
)

def build_final_approval_queue_item(ticket: ControlledPlanningTicket, rehearsal_run: Optional[PaperAdjacentRehearsalRun] = None) -> FinalHumanApprovalQueueItem:
    run_id = rehearsal_run.run_id if rehearsal_run else None
    return FinalHumanApprovalQueueItem(
        queue_item_id=create_final_approval_queue_item_id(),
        created_at_utc=_now_str(),
        status=ApprovalQueueItemStatus.QUEUED,
        candidate_id=ticket.candidate_id,
        planning_ticket_id=ticket.ticket_id,
        rehearsal_run_id=run_id,
        decision=ApprovalQueueDecision.INCONCLUSIVE,
        reviewer_notes=None,
        reviewer_id=None,
        reviewed_at_utc=None,
        required_evidence_refs=ticket.evidence_refs.copy(),
        safety_flags=ticket.safety_flags.copy(),
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def update_approval_queue_item_notes(item: FinalHumanApprovalQueueItem, reviewer_notes: str, reviewer_id: Optional[str] = None) -> FinalHumanApprovalQueueItem:
    item.reviewer_notes = reviewer_notes
    item.reviewer_id = reviewer_id
    item.reviewed_at_utc = _now_str()
    if item.status == ApprovalQueueItemStatus.QUEUED:
        item.status = ApprovalQueueItemStatus.REVIEWED_WITH_NOTES
    return item

def mark_approval_queue_item_for_next_non_executing_stage(item: FinalHumanApprovalQueueItem) -> FinalHumanApprovalQueueItem:
    item.status = ApprovalQueueItemStatus.APPROVED_FOR_NEXT_NON_EXECUTING_STAGE
    item.decision = ApprovalQueueDecision.APPROVE_FOR_NEXT_NON_EXECUTING_STAGE
    item.reviewed_at_utc = _now_str()
    return item

def reject_approval_queue_item(item: FinalHumanApprovalQueueItem, reason: str) -> FinalHumanApprovalQueueItem:
    item.status = ApprovalQueueItemStatus.REJECTED
    item.decision = ApprovalQueueDecision.REJECT
    item.reviewer_notes = f"{item.reviewer_notes}\nReject Reason: {reason}" if item.reviewer_notes else f"Reject Reason: {reason}"
    item.reviewed_at_utc = _now_str()
    return item

def block_approval_queue_item(item: FinalHumanApprovalQueueItem, reason: str) -> FinalHumanApprovalQueueItem:
    item.status = ApprovalQueueItemStatus.BLOCKED
    item.decision = ApprovalQueueDecision.BLOCK
    item.reviewer_notes = f"{item.reviewer_notes}\nBlock Reason: {reason}" if item.reviewer_notes else f"Block Reason: {reason}"
    item.reviewed_at_utc = _now_str()
    return item

def approval_queue_item_summary(item: FinalHumanApprovalQueueItem) -> dict[str, Any]:
    return {
        "queue_item_id": item.queue_item_id,
        "status": item.status.value,
        "candidate_id": item.candidate_id,
        "has_notes": bool(item.reviewer_notes)
    }

def approval_queue_item_to_text(item: FinalHumanApprovalQueueItem) -> str:
    lines = [
        "✅ FINAL HUMAN APPROVAL QUEUE ITEM",
        f"Item ID: {item.queue_item_id}",
        f"Status: {item.status.value}",
        f"Candidate ID: {item.candidate_id or 'Unknown'}",
        f"Decision: {item.decision.value}",
        f"Reviewer Notes: {item.reviewer_notes or 'Pending'}"
    ]
    lines.append("LIMITATION: Approval is ONLY for non-executing observer planning. It NEVER enables active paper trading.")
    return "\n".join(lines)
