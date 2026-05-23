
from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.exceptions import PaperSafeBoundaryIngestionError

def extract_boundary_certificate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("boundary_certificate")

def extract_blocker_replay_result(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("blocker_replay_result")

def extract_evidence_freeze_bundle(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("evidence_freeze_bundle")

def extract_boundary_rules(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("rules", [])

def extract_boundary_assertions(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("assertions", [])

def extract_boundary_candidate_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def extract_boundary_decision(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("decision")

def ingest_boundary_certificate_full_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = extract_boundary_decision(payload)
    if payload.get("activation_allowed", False):
        raise PaperSafeBoundaryIngestionError("activation_allowed must be false")
    if payload.get("admission_allowed", False):
        raise PaperSafeBoundaryIngestionError("admission_allowed must be false")
    if payload.get("transition_allowed", False):
        raise PaperSafeBoundaryIngestionError("transition_allowed must be false")
    if payload.get("order_created", False):
        raise PaperSafeBoundaryIngestionError("order_created must be false")
    if payload.get("mutation_detected", False):
        raise PaperSafeBoundaryIngestionError("mutation_detected must be false")

    return payload

def boundary_supports_paper_safe_gate(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def boundary_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return "Boundary Ingestion: Success"
