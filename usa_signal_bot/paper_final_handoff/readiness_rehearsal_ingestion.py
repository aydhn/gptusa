from typing import Any, Dict, Optional, Tuple
from usa_signal_bot.core.enums import FinalHandoffRiskFlag

def ingest_readiness_rehearsal_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.copy()

def extract_guarded_handoff_entry(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("guarded_handoff_registry_entry")

def extract_final_review_lock(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("final_review_lock")

def extract_rehearsal_run(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("staged_rehearsal_run")

def extract_candidate_id_from_rehearsal(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def readiness_rehearsal_supports_final_handoff(payload: Dict[str, Any]) -> Tuple[bool, list[str]]:
    warnings = []
    status = payload.get("status")
    if status in ["BLOCKED", "REJECTED"]:
        warnings.append("Rehearsal status is BLOCKED or REJECTED.")
        return False, warnings

    lock = extract_final_review_lock(payload)
    if not lock:
        warnings.append("Missing final_review_lock in rehearsal payload.")
        return False, warnings

    if status == "READY_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW":
        return True, warnings

    warnings.append(f"Unexpected rehearsal status: {status}")
    return False, warnings

def readiness_rehearsal_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return f"ReadinessRehearsalIngestion: candidate_id={payload.get('candidate_id')}, status={payload.get('status')}"
