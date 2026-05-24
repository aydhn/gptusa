import json
from typing import Any, Optional, Tuple, List
from usa_signal_bot.core.enums import PrePaperHandoffFreezeRiskFlag

def extract_simulator_dossier(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("simulator_dossier")

def extract_simulator_acceptance_seal(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("simulator_acceptance_seal")

def extract_sandbox_runtime_admission_blocker_events(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("sandbox_runtime_admission_blocker_events", [])

def extract_simulator_dossier_candidate_id(payload: dict[str, Any]) -> Optional[str]:
    dossier = extract_simulator_dossier(payload)
    if dossier:
        return dossier.get("candidate_id")
    return payload.get("candidate_id")

def extract_simulator_dossier_decision(payload: dict[str, Any]) -> Optional[str]:
    dossier = extract_simulator_dossier(payload)
    if dossier:
        return dossier.get("decision")
    return None

def simulator_dossier_supports_handoff_freeze(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    dossier = extract_simulator_dossier(payload)
    if not dossier:
        warnings.append("Missing simulator dossier")
        return False, warnings

    seal = extract_simulator_acceptance_seal(payload)
    if not seal:
        warnings.append("Missing simulator acceptance seal")
        return False, warnings

    if seal.get("status") not in ["VALIDATED", "SEALED"]:
        warnings.append("Simulator acceptance seal not validated/sealed")
        return False, warnings

    if not extract_sandbox_runtime_admission_blocker_events(payload):
        warnings.append("Missing sandbox runtime admission blocker events")
        return False, warnings

    if payload.get("sandbox_runtime_admission_allowed", False):
        warnings.append("sandbox_runtime_admission_allowed=True found")
        return False, warnings

    if payload.get("paper_sandbox_runtime_allowed", False):
        warnings.append("paper_sandbox_runtime_allowed=True found")
        return False, warnings

    if payload.get("simulator_admission_allowed", False):
        warnings.append("simulator_admission_allowed=True found")
        return False, warnings

    if payload.get("local_paper_simulator_allowed", False):
        warnings.append("local_paper_simulator_allowed=True found")
        return False, warnings

    if payload.get("activation_allowed", False):
        warnings.append("activation_allowed=True found")
        return False, warnings

    if payload.get("admission_allowed", False):
        warnings.append("admission_allowed=True found")
        return False, warnings

    if payload.get("transition_allowed", False):
        warnings.append("transition_allowed=True found")
        return False, warnings

    if payload.get("order_created", False):
        warnings.append("order_created=True found")
        return False, warnings

    if payload.get("mutation_detected", False):
        warnings.append("mutation_detected=True found")
        return False, warnings

    events = extract_sandbox_runtime_admission_blocker_events(payload)
    for e in events:
        if not e.get("blocked", True):
            warnings.append("Found unblocked sandbox runtime admission blocker event")
            return False, warnings

    decision = extract_simulator_dossier_decision(payload)
    if decision not in ["CREATE_SIMULATOR_DOSSIER", "VALIDATED_SIMULATOR_SAFE"]:
        warnings.append(f"Unexpected simulator dossier decision: {decision}")
        return False, warnings

    return True, warnings

def ingest_simulator_dossier_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    valid, warnings = simulator_dossier_supports_handoff_freeze(payload)
    return {
        "valid": valid,
        "warnings": warnings,
        "payload": payload
    }

def simulator_dossier_ingestion_to_text(payload: dict[str, Any]) -> str:
    valid, warnings = simulator_dossier_supports_handoff_freeze(payload)
    res = f"Simulator Dossier Ingestion: {'Valid' if valid else 'Invalid'}\n"
    if warnings:
        res += "Warnings:\n"
        for w in warnings:
            res += f"- {w}\n"
    return res
