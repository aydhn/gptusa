import json
from pathlib import Path
from typing import Any

def load_calendar_validation_metadata_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def calendar_validation_for_symbol(symbol: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get(symbol, [])

def calendar_anomalies_for_timestamp(symbol: str, timestamp: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    anomalies = calendar_validation_for_symbol(symbol, payload)
    return [a for a in anomalies if a.get("timestamp") == timestamp]

def validate_calendar_metadata(payload: dict[str, Any]) -> list[str]:
    return []

def calendar_metadata_loader_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"symbol_count": len(payload)}

def calendar_metadata_loader_to_text(payload: dict[str, Any], limit: int = 100) -> str:
    return f"Loaded calendar metadata for {len(payload)} symbols."
