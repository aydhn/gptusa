from typing import Any, List
from usa_signal_bot.core.enums import (
    ControlledPlanningDecision,
    ControlledPlanningTicketStatus,
    ControlledPlanningSafetyFlag
)
from usa_signal_bot.paper_controlled_planning.observation_ingestion import (
    extract_exit_decision,
    extract_observation_score,
    observation_supports_controlled_planning
)

def controlled_planning_safety_flags_from_observation(payload: dict[str, Any]) -> List[ControlledPlanningSafetyFlag]:
    flags = []
    decision = extract_exit_decision(payload)
    if decision in ["BLOCK", "REJECT", "REJECTED", "BLOCKED"]:
        flags.append(ControlledPlanningSafetyFlag.BLOCKED_EXIT_DECISION)
    if decision is None:
        flags.append(ControlledPlanningSafetyFlag.MISSING_OBSERVATION_EXIT_REVIEW)
    return flags

def evaluate_controlled_planning_eligibility(observation_payload: dict[str, Any], min_score: float = 75.0) -> ControlledPlanningDecision:
    flags = controlled_planning_safety_flags_from_observation(observation_payload)
    if ControlledPlanningSafetyFlag.BLOCKED_EXIT_DECISION in flags:
        return ControlledPlanningDecision.BLOCK

    supports, _ = observation_supports_controlled_planning(observation_payload)
    if not supports:
        decision = extract_exit_decision(observation_payload)
        if decision == "REQUEST_DRY_RUN_RETEST":
            return ControlledPlanningDecision.REQUEST_DRY_RUN_RETEST
        elif decision == "REQUEST_MANUAL_REVIEW":
            return ControlledPlanningDecision.REQUEST_MANUAL_REVIEW
        return ControlledPlanningDecision.REQUEST_MORE_OBSERVATION

    score = extract_observation_score(observation_payload)
    if score is not None and score >= min_score:
        return ControlledPlanningDecision.CREATE_PLANNING_TICKET

    if score is not None and score < min_score:
        return ControlledPlanningDecision.REQUEST_MORE_OBSERVATION

    return ControlledPlanningDecision.INCONCLUSIVE

def controlled_planning_eligibility_reasons(observation_payload: dict[str, Any], min_score: float = 75.0) -> List[str]:
    decision = evaluate_controlled_planning_eligibility(observation_payload, min_score)
    reasons = [f"Eligibility Decision: {decision.value}"]
    supports, obs_reasons = observation_supports_controlled_planning(observation_payload)
    reasons.extend(obs_reasons)
    score = extract_observation_score(observation_payload)
    if score is not None:
        reasons.append(f"Observation Score: {score} (min_score: {min_score})")
    else:
        reasons.append("Observation Score is missing.")
    return reasons

def planning_ticket_status_from_decision(decision: ControlledPlanningDecision) -> ControlledPlanningTicketStatus:
    if decision == ControlledPlanningDecision.CREATE_PLANNING_TICKET:
        return ControlledPlanningTicketStatus.CREATED
    elif decision == ControlledPlanningDecision.REJECT:
        return ControlledPlanningTicketStatus.REJECTED
    elif decision == ControlledPlanningDecision.BLOCK:
        return ControlledPlanningTicketStatus.BLOCKED
    else:
        return ControlledPlanningTicketStatus.DRAFT

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_controlled_planning_eligibility(payload)
    reasons = controlled_planning_eligibility_reasons(payload)
    lines = [
        "✅ ELIGIBILITY CHECKER",
        f"Decision: {decision.value}"
    ]
    for r in reasons:
        lines.append(f" - {r}")
    lines.append("LIMITATION: Planning eligibility does NOT imply live execution or paper enable.")
    return "\n".join(lines)
