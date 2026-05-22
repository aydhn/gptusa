
from typing import Any, Tuple, Optional
from usa_signal_bot.core.exceptions import PaperReadinessBoardConfirmationIngestionError

def ingest_readiness_confirmation_review(payload: dict) -> dict:
    return {"ingested_payload": payload, "status": "INGESTED", "metadata": {}}

def extract_confirmation_queue_item(payload: dict) -> Optional[dict]:
    return payload.get("confirmation_queue_item")

def extract_human_review_bundle(payload: dict) -> Optional[dict]:
    return payload.get("human_review_bundle")

def extract_activation_still_denied_registry_entry(payload: dict) -> Optional[dict]:
    return payload.get("activation_still_denied_registry_entry")

def extract_confirmation_candidate_id(payload: dict) -> Optional[str]:
    return payload.get("candidate_id")

def extract_activation_denied_state(payload: dict) -> Tuple[Optional[bool], Optional[bool]]:
    # return (activation_denied, activation_allowed)
    denied = payload.get("activation_denied")
    allowed = payload.get("activation_allowed")
    return denied, allowed

def readiness_confirmation_supports_board(payload: dict) -> Tuple[bool, list]:
    bundle = extract_human_review_bundle(payload)
    registry = extract_activation_still_denied_registry_entry(payload)
    if not bundle:
        return False, ["Missing human review bundle warning/block."]
    if not registry:
        return False, ["Missing activation-still-denied registry block."]
    denied, allowed = extract_activation_denied_state(payload)
    if allowed:
        return False, ["activation_allowed true ise block."]
    return True, []

def confirmation_ingestion_to_text(payload: dict) -> str:
    return str(payload)
