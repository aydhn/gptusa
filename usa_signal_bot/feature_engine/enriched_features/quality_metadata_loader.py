import json
from pathlib import Path
from typing import Any

def load_provider_quality_metadata_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def quality_metadata_for_symbol(symbol: str, payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get(symbol, {})

def source_trust_for_symbol(symbol: str, payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get(symbol, {}).get("source_trust", {})

def validate_quality_metadata(payload: dict[str, Any]) -> list[str]:
    return []

def quality_metadata_loader_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"symbol_count": len(payload)}

def quality_metadata_loader_to_text(payload: dict[str, Any], limit: int = 100) -> str:
    return f"Loaded quality metadata for {len(payload)} symbols."
