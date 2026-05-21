from typing import Any, Dict, List, Tuple
from datetime import datetime, timezone

def ingest_observer_governance_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.copy()

def extract_observer_governance_decision(payload: Dict[str, Any]) -> str | None:
    return payload.get("decision")

def extract_observer_governance_candidate_id(payload: Dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def extract_observer_governance_evidence_refs(payload: Dict[str, Any]) -> List[str]:
    return payload.get("evidence_refs", [])

def extract_observer_governance_risk_flags(payload: Dict[str, Any]) -> List[str]:
    return payload.get("risk_flags", [])

def observer_governance_supports_promotion_dossier(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    decision = extract_observer_governance_decision(payload)
    if decision == "ELIGIBLE_FOR_NON_EXECUTING_PROMOTION_DOSSIER":
        return True, []
    elif decision in ["BLOCK", "REJECT"]:
        return False, ["Observer governance returned blocking/reject decision."]
    return False, ["Observer governance decision not suitable or missing."]

def observer_governance_ingestion_to_text(payload: Dict[str, Any]) -> str:
    decision = extract_observer_governance_decision(payload)
    candidate_id = extract_observer_governance_candidate_id(payload)
    return f"Ingested governance review for candidate {candidate_id} with decision {decision}."
