import json
from pathlib import Path
from typing import Any, Dict, List

def load_ml_source_registry_json(path: Path) -> Dict[str, Any]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    with open(path, "r") as f:
        return json.load(f)

def load_ml_dataset_contract_json(path: Path) -> Dict[str, Any]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    with open(path, "r") as f:
        return json.load(f)

def load_ml_feature_contracts_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    results = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results

def load_ml_target_contracts_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    results = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results

def load_ml_label_contracts_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    results = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results

def load_ml_leakage_guard_json(path: Path) -> Dict[str, Any]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    with open(path, "r") as f:
        return json.load(f)

def load_ml_non_activation_boundary_json(path: Path) -> Dict[str, Any]:
    if not path.is_absolute() and ".." in str(path):
        raise ValueError("Path traversal detected")
    with open(path, "r") as f:
        return json.load(f)

def validate_ml_foundation_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []
    for k, v in payloads.items():
        v_str = str(v).lower()
        if "training_started': true" in v_str or "training_started\": true" in v_str:
            errors.append(f"Forbidden training_started flag in {k}")
        if "prediction_started': true" in v_str or "prediction_started\": true" in v_str:
            errors.append(f"Forbidden prediction_started flag in {k}")
        if "daemon_started': true" in v_str or "daemon_started\": true" in v_str:
            errors.append(f"Forbidden daemon_started flag in {k}")
        if "scheduler_enabled': true" in v_str or "scheduler_enabled\": true" in v_str:
            errors.append(f"Forbidden scheduler_enabled flag in {k}")
        if "buy" in v_str and "signal" in v_str:
            errors.append(f"Forbidden buy signal terminology in {k}")
        if "sell" in v_str and "signal" in v_str:
            errors.append(f"Forbidden sell signal terminology in {k}")
        if "order" in v_str and "decision" in v_str:
            errors.append(f"Forbidden order decision terminology in {k}")
        if "portfolio" in v_str and "weight" in v_str:
            errors.append(f"Forbidden portfolio weight terminology in {k}")
    return errors

def ml_foundation_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_keys": list(payloads.keys()),
        "total_artifacts": len(payloads)
    }

def ml_foundation_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    s = json.dumps(ml_foundation_artifact_loader_summary(payloads), indent=2)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
