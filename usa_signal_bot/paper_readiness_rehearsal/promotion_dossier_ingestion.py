from typing import Any, Dict, Optional, Tuple

def ingest_promotion_dossier_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Mocking ingestion process without altering state
    return payload.copy()

def extract_readiness_package(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    packages = payload.get("readiness_packages", [])
    if packages:
        return packages[-1]
    return None

def extract_readiness_package_id(payload: Dict[str, Any]) -> Optional[str]:
    pkg = extract_readiness_package(payload)
    if pkg:
        return pkg.get("package_id")
    return None

def extract_candidate_id_from_dossier(payload: Dict[str, Any]) -> Optional[str]:
    dossiers = payload.get("dossiers", [])
    if dossiers:
        return dossiers[-1].get("candidate_id")
    return None

def extract_safety_board_decision(payload: Dict[str, Any]) -> Optional[str]:
    reviews = payload.get("board_reviews", [])
    if reviews:
        return reviews[-1].get("decision")
    return None

def promotion_dossier_supports_readiness_rehearsal(payload: Dict[str, Any]) -> Tuple[bool, list[str]]:
    reasons = []
    decision = extract_safety_board_decision(payload)
    pkg = extract_readiness_package(payload)

    if decision == "PASS_FOR_STAGED_NON_EXECUTING_READINESS_PACKAGE":
        if pkg:
            return True, ["Safety board passed and readiness package available."]
        else:
            return False, ["Missing readiness package warning."]

    if decision in ["BLOCK", "REJECT", "BLOCK_DOSSIER", "REJECT_DOSSIER"]:
        return False, ["Safety board blocked or rejected."]

    return False, ["Inconclusive safety board decision or missing data."]

def promotion_dossier_ingestion_to_text(payload: Dict[str, Any]) -> str:
    support, msgs = promotion_dossier_supports_readiness_rehearsal(payload)
    msg_str = ", ".join(msgs)
    return f"Promotion Dossier Ingestion: Supports Rehearsal={support}. Messages: {msg_str}"
