from typing import Any, Dict, List, Tuple, Optional
import json

def ingest_dry_admission_full_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "activation_allowed" in payload and payload.get("activation_allowed"):
        payload["warnings"] = payload.get("warnings", []) + ["activation_allowed is true, blocking"]
    if "all_writes_blocked" in payload and not payload.get("all_writes_blocked"):
        payload["warnings"] = payload.get("warnings", []) + ["all_writes_blocked is false, blocking"]
    if "mutation_detected" in payload and payload.get("mutation_detected"):
        payload["warnings"] = payload.get("warnings", []) + ["mutation_detected is true, blocking"]

    human_ledger = extract_human_approval_ledger(payload)
    if not human_ledger:
        payload["warnings"] = payload.get("warnings", []) + ["Missing human ledger"]

    write_lock = extract_write_lock_refresh(payload)
    if not write_lock:
        payload["warnings"] = payload.get("warnings", []) + ["Missing write-lock refresh"]

    return payload

def extract_dry_admission_run(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("dry_admission_run")

def extract_write_lock_refresh(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("write_lock_refresh")

def extract_human_approval_ledger(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("human_approval_ledger")

def extract_dry_admission_candidate_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def extract_dry_admission_decision(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("decision")

def dry_admission_supports_admission_review(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    supported = True

    if not payload:
        return False, ["Payload is empty"]

    decision = extract_dry_admission_decision(payload)
    if decision not in ["RUN_DRY_ADMISSION_REHEARSAL", "COMPLETED_NO_WRITE"]:
        warnings.append(f"Invalid decision for admission review: {decision}")
        supported = False

    return supported, warnings

def dry_admission_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
