from typing import Any, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket,
    ControlledPlanningReview,
    ControlledPlanningReportType
)
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket_from_observation
from usa_signal_bot.paper_controlled_planning.planning_report import build_controlled_planning_review

def planning_ticket_from_observation_review(payload: dict[str, Any]) -> ControlledPlanningTicket:
    return build_controlled_planning_ticket_from_observation(payload)

def planning_review_from_observation_review(payload: dict[str, Any], paper_snapshot: Optional[dict[str, Any]] = None) -> ControlledPlanningReview:
    ticket = planning_ticket_from_observation_review(payload)
    return build_controlled_planning_review(ticket)

def attach_planning_metadata_to_observation_payload(payload: dict[str, Any], review: ControlledPlanningReview) -> dict[str, Any]:
    payload["controlled_planning_review_id"] = review.review_id
    if review.planning_tickets:
        payload["planning_ticket_id"] = review.planning_tickets[0].ticket_id
        payload["planning_ticket_status"] = review.planning_tickets[0].status.value
    return payload

def paper_observation_planning_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": payload.get("candidate_id"),
        "has_planning_ticket": "planning_ticket_id" in payload,
        "planning_ticket_status": payload.get("planning_ticket_status")
    }

def paper_observation_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = paper_observation_planning_summary(payload)
    lines = [
        "🔄 PAPER OBSERVATION TO CONTROLLED PLANNING ADAPTER",
        f"Candidate ID: {summary['candidate_id'] or 'Unknown'}",
        f"Has Planning Ticket: {summary['has_planning_ticket']}",
        f"Planning Ticket Status: {summary['planning_ticket_status'] or 'N/A'}",
        "LIMITATION: This adapter only generates planning metadata. It does NOT enable active paper trading."
    ]
    return "\n".join(lines)
