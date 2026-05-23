from typing import Any
import json

def ingest_no_order_dossier_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

def extract_no_order_dossier(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("dossier")

def extract_bridge_replay_audit_seal(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("bridge_replay_audit_seal")

def extract_admission_blocker_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("admission_blocker_events", [])

def extract_no_order_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def extract_no_order_decision(payload: dict[str, Any]) -> str | None:
    return payload.get("decision")

def no_order_supports_boundary_certificate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []

    dossier = extract_no_order_dossier(payload)
    if not dossier:
        warnings.append("Missing no_order_dossier")
        return False, warnings

    seal = extract_bridge_replay_audit_seal(payload)
    if not seal:
        warnings.append("Missing bridge_replay_audit_seal")

    events = extract_admission_blocker_events(payload)
    if not events:
        warnings.append("Missing admission_blocker_events")

    if payload.get("activation_allowed", False):
        warnings.append("activation_allowed is true")
        return False, warnings

    if payload.get("admission_allowed", False):
        warnings.append("admission_allowed is true")
        return False, warnings

    if payload.get("transition_allowed", False):
        warnings.append("transition_allowed is true")
        return False, warnings

    if payload.get("order_created", False):
        warnings.append("order_created is true")
        return False, warnings

    if payload.get("mutation_detected", False):
        warnings.append("mutation_detected is true")
        return False, warnings

    for ev in events:
        if not ev.get("blocked", True):
            warnings.append("admission blocker event blocked=false")
            return False, warnings

    if warnings:
        return False, warnings

    return True, []

def no_order_ingestion_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
