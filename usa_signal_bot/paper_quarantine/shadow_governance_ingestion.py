from typing import Any

from usa_signal_bot.core.exceptions import ShadowGovernanceIngestionError

def ingest_shadow_governance_review(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload:
        raise ShadowGovernanceIngestionError("Payload cannot be empty")
    return payload.copy()

def extract_shadow_governance_decision(payload: dict[str, Any]) -> str | None:
    return payload.get("decision") or payload.get("governance_decision")

def extract_shadow_acceptance_score(payload: dict[str, Any]) -> float | None:
    score = payload.get("acceptance_score") or payload.get("score")
    if score is not None:
        try:
            return float(score)
        except ValueError:
            return None
    return None

def extract_shadow_risk_flags(payload: dict[str, Any]) -> list[str]:
    return payload.get("risk_flags", [])

def extract_shadow_required_followups(payload: dict[str, Any]) -> list[str]:
    return payload.get("required_followups", [])

def shadow_governance_supports_quarantine(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    decision = extract_shadow_governance_decision(payload)
    if decision == "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE":
        return True, []
    elif decision in ["BLOCK", "REJECT"]:
        return False, ["Shadow governance decision blocks quarantine enrollment."]
    return False, ["Missing or inconclusive shadow governance decision."]

def shadow_governance_ingestion_to_text(payload: dict[str, Any]) -> str:
    decision = extract_shadow_governance_decision(payload)
    score = extract_shadow_acceptance_score(payload)
    flags = extract_shadow_risk_flags(payload)

    lines = [
        f"Shadow Governance Decision: {decision}",
        f"Acceptance Score: {score}",
        f"Risk Flags: {flags}",
    ]
    return "\n".join(lines)
