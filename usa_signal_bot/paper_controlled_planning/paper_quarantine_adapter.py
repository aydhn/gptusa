from typing import Any, Tuple, List
from usa_signal_bot.paper_controlled_planning.planning_models import ControlledPlanningReview

def controlled_planning_refs_from_quarantine_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": payload.get("candidate_id"),
        "quarantine_status": payload.get("status"),
        "planning_ticket_id": payload.get("planning_ticket_id")
    }

def quarantine_supports_controlled_planning(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    status = payload.get("status")
    if status == "EXIT_ELIGIBLE":
        reasons.append("Quarantine status EXIT_ELIGIBLE supports controlled planning.")
        return True, reasons

    reasons.append(f"Quarantine status {status} does NOT support controlled planning yet.")
    return False, reasons

def attach_controlled_planning_metadata_to_quarantine_payload(payload: dict[str, Any], review: ControlledPlanningReview) -> dict[str, Any]:
    if review.planning_tickets:
        payload["planning_ticket_id"] = review.planning_tickets[0].ticket_id
    payload["planning_review_id"] = review.review_id
    return payload

def paper_quarantine_planning_summary(payload: dict[str, Any]) -> dict[str, Any]:
    supports, _ = quarantine_supports_controlled_planning(payload)
    return {
        "candidate_id": payload.get("candidate_id"),
        "quarantine_status": payload.get("status"),
        "supports_planning": supports
    }

def paper_quarantine_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = paper_quarantine_planning_summary(payload)
    lines = [
        "🔄 PAPER QUARANTINE TO CONTROLLED PLANNING ADAPTER",
        f"Candidate ID: {summary['candidate_id'] or 'Unknown'}",
        f"Quarantine Status: {summary['quarantine_status'] or 'Unknown'}",
        f"Supports Planning: {summary['supports_planning']}"
    ]
    return "\n".join(lines)
