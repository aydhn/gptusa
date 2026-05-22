from typing import Any

def ingest_firewall_audit_review(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return payload.copy()

def extract_readiness_audit_checkpoint(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("readiness_audit_checkpoint")

def extract_firewall_replay_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("firewall_replay_result")

def extract_zero_mutation_audit(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("zero_mutation_audit")

def extract_pre_paper_evidence_refresh(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("pre_paper_evidence_refresh")

def extract_firewall_audit_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def firewall_audit_supports_readiness_confirmation(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []

    if payload.get("decision") != "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT":
        reasons.append("Decision is not CONTINUE_WITH_ACTIVATION_DENIED_AUDIT")

    if payload.get("activation_allowed") is True:
        reasons.append("activation_allowed must be false")

    zero = extract_zero_mutation_audit(payload)
    if zero and zero.get("status") == "FAILED":
        reasons.append("zero_mutation_audit status is FAILED")

    return len(reasons) == 0, reasons

def firewall_audit_ingestion_to_text(payload: dict[str, Any]) -> str:
    supports, reasons = firewall_audit_supports_readiness_confirmation(payload)
    return f"Supports Readiness Confirmation: {supports}\nReasons: {reasons}"
