from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket,
    create_controlled_planning_ticket_id,
    _now_str
)
from usa_signal_bot.core.enums import (
    ControlledPlanningTicketStatus,
    ControlledPlanningSafetyFlag
)
from usa_signal_bot.paper_controlled_planning.observation_ingestion import (
    extract_observation_candidate_id,
    extract_observation_score,
    extract_exit_decision,
    extract_quarantine_exit_review
)
from usa_signal_bot.paper_controlled_planning.eligibility_checker import (
    evaluate_controlled_planning_eligibility,
    planning_ticket_status_from_decision,
    controlled_planning_safety_flags_from_observation
)

def build_controlled_planning_ticket(
    candidate_id: Optional[str],
    observation_score: Optional[float],
    exit_decision: Optional[str],
    evidence_refs: Optional[List[str]] = None
) -> ControlledPlanningTicket:
    status = ControlledPlanningTicketStatus.DRAFT
    if exit_decision == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING":
        status = ControlledPlanningTicketStatus.CREATED
    elif exit_decision in ["BLOCK", "REJECT", "REJECTED", "BLOCKED"]:
        status = ControlledPlanningTicketStatus.BLOCKED

    flags = []
    if exit_decision in ["BLOCK", "REJECT", "REJECTED", "BLOCKED"]:
        flags.append(ControlledPlanningSafetyFlag.BLOCKED_EXIT_DECISION)
    if not exit_decision:
        flags.append(ControlledPlanningSafetyFlag.MISSING_OBSERVATION_EXIT_REVIEW)

    return ControlledPlanningTicket(
        ticket_id=create_controlled_planning_ticket_id(),
        created_at_utc=_now_str(),
        status=status,
        candidate_id=candidate_id,
        source_observation_review_id=None,
        source_exit_review_id=None,
        source_exit_decision=exit_decision,
        observation_score=observation_score,
        evidence_refs=evidence_refs or [],
        required_followups=[],
        safety_flags=flags,
        manual_review_required=True,
        final_approval_required=True,
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_config_patch=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def build_controlled_planning_ticket_from_observation(payload: dict[str, Any]) -> ControlledPlanningTicket:
    decision_enum = evaluate_controlled_planning_eligibility(payload)
    status = planning_ticket_status_from_decision(decision_enum)
    flags = controlled_planning_safety_flags_from_observation(payload)

    exit_review = extract_quarantine_exit_review(payload)
    exit_review_id = exit_review.get("review_id") if exit_review else None

    return ControlledPlanningTicket(
        ticket_id=create_controlled_planning_ticket_id(),
        created_at_utc=_now_str(),
        status=status,
        candidate_id=extract_observation_candidate_id(payload),
        source_observation_review_id=payload.get("review_id"),
        source_exit_review_id=exit_review_id,
        source_exit_decision=extract_exit_decision(payload),
        observation_score=extract_observation_score(payload),
        evidence_refs=[],
        required_followups=[],
        safety_flags=flags,
        manual_review_required=True,
        final_approval_required=True,
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_config_patch=False,
        warnings=[],
        errors=[],
        metadata={"eligibility_decision": decision_enum.value}
    )

def validate_planning_ticket_safety(ticket: ControlledPlanningTicket) -> List[str]:
    errors = []
    if ticket.allowed_for_active_paper: errors.append("Ticket allowed_for_active_paper is True")
    if ticket.allowed_for_broker_execution: errors.append("Ticket allowed_for_broker_execution is True")
    if ticket.allowed_for_paper_state_mutation: errors.append("Ticket allowed_for_paper_state_mutation is True")
    if ticket.allowed_for_config_patch: errors.append("Ticket allowed_for_config_patch is True")
    return errors

def planning_ticket_summary(ticket: ControlledPlanningTicket) -> dict[str, Any]:
    return {
        "ticket_id": ticket.ticket_id,
        "status": ticket.status.value,
        "candidate_id": ticket.candidate_id,
        "safety_flags": [f.value for f in ticket.safety_flags]
    }

def planning_ticket_to_text(ticket: ControlledPlanningTicket) -> str:
    lines = [
        "🎫 CONTROLLED PLANNING TICKET",
        f"Ticket ID: {ticket.ticket_id}",
        f"Status: {ticket.status.value}",
        f"Candidate ID: {ticket.candidate_id or 'Unknown'}",
        f"Observation Score: {ticket.observation_score if ticket.observation_score is not None else 'N/A'}",
        f"Exit Decision: {ticket.source_exit_decision or 'N/A'}",
        f"Safety Flags: {', '.join([f.value for f in ticket.safety_flags]) if ticket.safety_flags else 'None'}"
    ]
    errs = validate_planning_ticket_safety(ticket)
    if errs:
        lines.append("SAFETY ERRORS:")
        for e in errs:
            lines.append(f" - {e}")
    lines.append("LIMITATION: A planning ticket is NOT an activation approval and NEVER triggers paper mutation or broker orders.")
    return "\n".join(lines)
