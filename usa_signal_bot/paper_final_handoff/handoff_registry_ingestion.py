from typing import Any, Dict, Optional

def ingest_guarded_handoff_registry_entry(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.copy()

def extract_handoff_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("handoff_id")

def extract_handoff_status(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("status")

def extract_handoff_decision(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("decision")

def validate_handoff_registry_entry_for_final_review(payload: Dict[str, Any]) -> list[str]:
    errors = []
    if payload.get("allows_active_paper", False):
        errors.append("Registry entry allows_active_paper is True.")
    if payload.get("allows_broker_execution", False):
        errors.append("Registry entry allows_broker_execution is True.")
    if payload.get("allows_paper_state_mutation", False):
        errors.append("Registry entry allows_paper_state_mutation is True.")
    if payload.get("allows_config_patch", False):
        errors.append("Registry entry allows_config_patch is True.")
    return errors

def handoff_registry_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return f"HandoffRegistryIngestion: handoff_id={payload.get('handoff_id')}, status={payload.get('status')}"
