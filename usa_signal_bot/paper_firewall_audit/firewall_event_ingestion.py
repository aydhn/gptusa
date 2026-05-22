from typing import Any, List
import copy

def ingest_firewall_events(events: List[dict[str, Any]]) -> List[dict[str, Any]]:
    return [normalize_firewall_event(e) for e in events]

def normalize_firewall_event(event: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(event)

def extract_attempt_types_from_events(events: List[dict[str, Any]]) -> List[str]:
    return list(set(e.get("attempt_type", "UNKNOWN") for e in events))

def count_blocked_events(events: List[dict[str, Any]]) -> int:
    return sum(1 for e in events if e.get("blocked", False))

def count_unblocked_dangerous_events(events: List[dict[str, Any]]) -> int:
    return sum(1 for e in events if not e.get("blocked", False) and e.get("is_dangerous", False))

def firewall_event_ingestion_warnings(events: List[dict[str, Any]]) -> List[str]:
    warnings = []
    if not events:
        warnings.append("No events found")
    unblocked = count_unblocked_dangerous_events(events)
    if unblocked > 0:
        warnings.append(f"Found {unblocked} unblocked dangerous events")
    return warnings

def firewall_event_ingestion_to_text(events: List[dict[str, Any]]) -> str:
    return f"Ingested {len(events)} events ({count_blocked_events(events)} blocked)"
