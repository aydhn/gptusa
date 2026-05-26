import json
from pathlib import Path
from typing import Any

def load_event_context_metadata_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_event_impact_metadata_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def event_context_for_symbol(symbol: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get(symbol, [])

def event_context_for_timestamp(symbol: str, timestamp: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    events = event_context_for_symbol(symbol, payload)
    return [e for e in events if e.get("timestamp") == timestamp]

def validate_event_context_metadata(payload: dict[str, Any]) -> list[str]:
    return []

def event_context_loader_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"symbol_count": len(payload)}

def event_context_loader_to_text(payload: dict[str, Any], limit: int = 100) -> str:
    return f"Loaded event context for {len(payload)} symbols."
