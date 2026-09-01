import json
from pathlib import Path
from typing import Any

def load_phase153_handoff_package_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_phase153_handoff_contract_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_phase153_readiness_gate_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_handoff_safety_boundary_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_metric_inventory_jsonl(path: Path) -> list[dict[str, Any]]:
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_risk_notes_jsonl(path: Path) -> list[dict[str, Any]]:
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def validate_phase153_handoff_payload(payload: dict[str, Any]) -> list[str]:
    errors = []

    if ".." in str(payload):
        # Extremely basic path traversal check simulation
        errors.append("Path traversal detected: '..' found in payload")

    for key in ["target_weight", "allocation", "position_size", "order", "live_signal"]:
        if key in payload:
            errors.append(f"Forbidden key found in handoff payload: {key}")

    # Check string representation for dangerous fields
    s_payload = str(payload)
    for term in ["target_weight", "allocation", "position_size", "order", "live_signal"]:
        if f"'{term}'" in s_payload or f'"{term}"' in s_payload:
            errors.append(f"Forbidden term found in handoff payload string: {term}")

    return errors

def phase153_handoff_loader_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "keys": list(payload.keys()),
        "valid": len(validate_phase153_handoff_payload(payload)) == 0
    }

def phase153_handoff_loader_to_text(payload: dict[str, Any], limit: int = 300) -> str:
    s = str(payload)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
