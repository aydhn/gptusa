from typing import Any

from usa_signal_bot.core.enums import PromotionTicketStatus
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
)

def manual_review_required_for_quarantine(candidate: QuarantinedPaperCandidate, ticket: ReadOnlyPromotionTicket | None = None) -> bool:
    if ticket and ticket.manual_review_completed:
        return False
    # Manual review is strictly required by default
    return True

def manual_review_gate_status(ticket: ReadOnlyPromotionTicket | None = None) -> str:
    if not ticket:
        return "WAITING_TICKET"
    if ticket.manual_review_completed:
        return "COMPLETED"
    if ticket.status == PromotionTicketStatus.WAITING_REVIEW:
        return "WAITING_REVIEW"
    return "REQUIRED"

def build_manual_review_requirements(candidate: QuarantinedPaperCandidate) -> list[str]:
    reqs = [
        "Review shadow governance acceptance score and decision.",
        "Review safety flags for broker/paper mutation risks.",
        "Ensure no automated active paper enrollment.",
        "Verify quarantine output isolation path."
    ]
    if candidate.risk_flags:
        reqs.append(f"Clear safety flags: {[f.value for f in candidate.risk_flags]}")
    return reqs

def apply_manual_review_placeholder(ticket: ReadOnlyPromotionTicket, completed: bool = False) -> ReadOnlyPromotionTicket:
    # Even if completed=True, this does NOT active paper.
    ticket.manual_review_completed = completed
    if completed:
        ticket.status = PromotionTicketStatus.APPROVED_FOR_SUPERVISED_DRY_RUN_PLANNING
    return ticket

def manual_review_gate_to_text(payload: dict[str, Any]) -> str:
    status = payload.get("status", "UNKNOWN")
    reqs = payload.get("requirements", [])

    lines = [
        f"Manual Review Gate Status: {status}",
        f"Requirements: {reqs}"
    ]
    return "\n".join(lines)
