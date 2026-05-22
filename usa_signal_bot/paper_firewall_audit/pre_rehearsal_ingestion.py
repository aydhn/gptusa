import json
from typing import Any, Tuple, List, Optional
import copy

def ingest_pre_paper_rehearsal_review(payload: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(payload)

def extract_pre_paper_run(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("pre_paper_run")

def extract_activation_denied_checkpoint(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("activation_denied_checkpoint")

def extract_firewall_events(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("firewall_events", [])

def extract_firewall_rules(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("firewall_rules", [])

def extract_pre_paper_candidate_id(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def pre_rehearsal_supports_firewall_audit(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    checkpoint = extract_activation_denied_checkpoint(payload)
    if not checkpoint:
        warnings.append("Missing activation-denied checkpoint")
    events = extract_firewall_events(payload)
    if not events:
        warnings.append("Missing firewall events")

    return len(warnings) == 0, warnings

def pre_rehearsal_ingestion_to_text(payload: dict[str, Any]) -> str:
    events = extract_firewall_events(payload)
    return f"PreRehearsal Ingestion: {len(events)} events"
