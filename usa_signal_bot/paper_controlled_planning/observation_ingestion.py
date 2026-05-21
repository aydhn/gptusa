from typing import Any, Tuple, List
from usa_signal_bot.core.exceptions import ControlledPlanningObservationIngestionError

def ingest_observation_review(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload:
        raise ControlledPlanningObservationIngestionError("Payload is empty.")
    return payload

def extract_quarantine_exit_review(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("quarantine_exit_review")

def extract_exit_decision(payload: dict[str, Any]) -> str | None:
    exit_review = extract_quarantine_exit_review(payload)
    if exit_review:
        return exit_review.get("decision")
    return payload.get("exit_decision")

def extract_observation_score(payload: dict[str, Any]) -> float | None:
    return payload.get("observation_score")

def extract_observation_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def observation_supports_controlled_planning(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    decision = extract_exit_decision(payload)
    if decision == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING":
        reasons.append("Observation exit decision is eligible for controlled planning.")
        return True, reasons
    if decision in ["BLOCK", "REJECT", "REJECTED", "BLOCKED"]:
        reasons.append(f"Observation exit decision {decision} blocks controlled planning.")
        return False, reasons
    reasons.append("Missing observation review or unknown decision.")
    return False, reasons

def observation_ingestion_to_text(payload: dict[str, Any]) -> str:
    candidate_id = extract_observation_candidate_id(payload)
    decision = extract_exit_decision(payload)
    score = extract_observation_score(payload)
    lines = [
        "🔍 OBSERVATION INGESTION",
        f"Candidate ID: {candidate_id or 'Unknown'}",
        f"Exit Decision: {decision or 'Unknown'}",
        f"Observation Score: {score if score is not None else 'Unknown'}",
    ]
    supports, reasons = observation_supports_controlled_planning(payload)
    lines.append(f"Supports Planning: {supports}")
    for r in reasons:
        lines.append(f" - {r}")
    lines.append("LIMITATION: Observation ingestion does NOT mutate paper state.")
    return "\n".join(lines)
