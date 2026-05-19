from typing import Any, Dict, List, Tuple

def ingest_release_candidate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload

def ingest_governance_review_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload

def extract_release_candidate_ids(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"candidate_id": payload.get("candidate_id"), "experiment_id": payload.get("experiment_id")}

def extract_governance_artifact_refs(payload: Dict[str, Any]) -> List[str]:
    return payload.get("artifact_refs", [])

def extract_governance_safety_flags(payload: Dict[str, Any]) -> List[str]:
    return payload.get("safety_flags", [])

def governance_candidate_packaging_allowed(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    if payload.get("allowed_for_auto_apply", False):
        reasons.append("Auto apply is not allowed for release packaging.")
    if payload.get("allowed_for_live_or_demo_execution", False):
        reasons.append("Live/demo execution is not allowed for release packaging.")

    return len(reasons) == 0, reasons

def governance_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return "Ingestion payload normalized."
