from typing import Any, List
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket,
    PaperAdjacentRehearsalContext,
    PaperAdjacentProposal,
    PaperAdjacentRehearsalRun,
    FinalHumanApprovalQueueItem,
    ControlledPlanningAuditEntry,
    ControlledPlanningReview
)
from usa_signal_bot.paper_controlled_planning.planning_ticket import planning_ticket_to_text
from usa_signal_bot.paper_controlled_planning.adjacent_rehearsal_context import adjacent_context_to_text
from usa_signal_bot.paper_controlled_planning.adjacent_proposal_builder import adjacent_proposals_to_text
from usa_signal_bot.paper_controlled_planning.guarded_rehearsal_runner import rehearsal_run_summary
from usa_signal_bot.paper_controlled_planning.approval_queue import approval_queue_item_to_text
from usa_signal_bot.paper_controlled_planning.planning_audit import controlled_planning_audit_to_text
from usa_signal_bot.paper_controlled_planning.planning_report import controlled_planning_review_to_text, controlled_planning_limitations_text

def paper_adjacent_proposal_to_text(item: PaperAdjacentProposal) -> str:
    return adjacent_proposals_to_text([item])

def paper_adjacent_rehearsal_run_to_text(item: PaperAdjacentRehearsalRun, limit: int = 100) -> str:
    summary = rehearsal_run_summary(item)
    lines = [
        "🏃‍♂️ PAPER-ADJACENT REHEARSAL RUN",
        f"Run ID: {summary['run_id']}",
        f"Status: {summary['status']}",
        f"Is Safe: {summary['is_safe']}",
        f"Proposals: {summary['proposal_count']}"
    ]
    if not summary['is_safe']:
        lines.append("⚠️ Run contains unsafe operations and was blocked or flagged.")
    return "\n".join(lines)

def controlled_planning_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "💾 CONTROLLED PLANNING STORE SUMMARY",
        f"Tickets: {summary.get('tickets_count', 0)}",
        f"Rehearsals: {summary.get('rehearsals_count', 0)}",
        f"Approval Queue Items: {summary.get('approval_queue_count', 0)}",
        f"Reviews: {summary.get('reviews_count', 0)}"
    ]
    return "\n".join(lines)
