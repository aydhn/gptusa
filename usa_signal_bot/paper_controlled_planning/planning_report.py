from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningReview,
    ControlledPlanningTicket,
    PaperAdjacentRehearsalRun,
    FinalHumanApprovalQueueItem,
    create_controlled_planning_review_id,
    _now_str
)
from usa_signal_bot.core.enums import ControlledPlanningReportType
from usa_signal_bot.paper_controlled_planning.planning_audit import (
    audit_entry_from_planning_ticket,
    audit_entry_from_approval_queue_item
)

def build_controlled_planning_review(
    ticket: ControlledPlanningTicket,
    rehearsal_run: Optional[PaperAdjacentRehearsalRun] = None,
    queue_item: Optional[FinalHumanApprovalQueueItem] = None
) -> ControlledPlanningReview:

    audits = [audit_entry_from_planning_ticket(ticket)]
    if queue_item:
        audits.append(audit_entry_from_approval_queue_item(queue_item))

    return ControlledPlanningReview(
        review_id=create_controlled_planning_review_id(),
        created_at_utc=_now_str(),
        report_type=ControlledPlanningReportType.FULL_CONTROLLED_PLANNING_REVIEW,
        planning_tickets=[ticket],
        rehearsal_runs=[rehearsal_run] if rehearsal_run else [],
        approval_queue_items=[queue_item] if queue_item else [],
        audit_entries=audits,
        output_paths={},
        warnings=[],
        errors=[]
    )

def controlled_planning_review_summary(review: ControlledPlanningReview) -> dict[str, Any]:
    ticket_status = review.planning_tickets[0].status.value if review.planning_tickets else "None"
    queue_status = review.approval_queue_items[0].status.value if review.approval_queue_items else "None"
    return {
        "review_id": review.review_id,
        "ticket_status": ticket_status,
        "queue_status": queue_status,
        "rehearsal_count": len(review.rehearsal_runs),
        "audit_count": len(review.audit_entries)
    }

def controlled_planning_limitations_text() -> str:
    lines = [
        "⚠️ CONTROLLED PLANNING LIMITATIONS:",
        "1. No real broker orders or live executions.",
        "2. No active paper trading enable.",
        "3. No real paper state mutation.",
        "4. No real Telegram sends (dry-run previews only).",
        "5. No production configuration writes.",
        "6. Final human approval queue is NOT a deployment approval.",
        "7. Results do NOT constitute investment advice."
    ]
    return "\n".join(lines)

def controlled_planning_review_to_text(review: ControlledPlanningReview, limit: int = 100) -> str:
    summary = controlled_planning_review_summary(review)
    lines = [
        "📊 FULL CONTROLLED PLANNING REVIEW",
        f"Review ID: {summary['review_id']}",
        f"Ticket Status: {summary['ticket_status']}",
        f"Queue Status: {summary['queue_status']}",
        f"Rehearsals: {summary['rehearsal_count']}",
        f"Audits: {summary['audit_count']}",
        "",
        controlled_planning_limitations_text()
    ]
    return "\n".join(lines)
