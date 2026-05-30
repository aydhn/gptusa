import json
from pathlib import Path
from typing import Any, Dict, List
from usa_signal_bot.core.exceptions import ContextValidationArtifactLoaderError

def _validate_path(path: Path) -> Path:
    resolved = path.resolve()
    if ".." in str(path):
        raise ContextValidationArtifactLoaderError(f"Path traversal detected: {path}")
    return resolved

def _check_unsafe_language(text: str) -> None:
    unsafe_words = ["buy_signal", "sell_signal", "entry", "exit", "order", "portfolio_weight", "target_weight", "allocation", "live_order", "demo_order"]
    for w in unsafe_words:
        if w in text.lower():
            raise ContextValidationArtifactLoaderError(f"Unsafe execution language found: {w}")

def load_compatibility_validation_result_json(path: Path) -> Dict[str, Any]:
    p = _validate_path(path)
    if not p.exists():
        raise ContextValidationArtifactLoaderError(f"File not found: {p}")
    with open(p, "r") as f:
        data = json.load(f)
    _check_unsafe_language(json.dumps(data))
    return data

def load_conditional_diagnostics_jsonl(path: Path) -> List[Dict[str, Any]]:
    p = _validate_path(path)
    if not p.exists():
        raise ContextValidationArtifactLoaderError(f"File not found: {p}")
    res = []
    with open(p, "r") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                _check_unsafe_language(json.dumps(data))
                res.append(data)
    return res

def load_conditional_diagnostics_profiles_jsonl(path: Path) -> List[Dict[str, Any]]:
    return load_conditional_diagnostics_jsonl(path)

def load_acceptance_gate_json(path: Path) -> Dict[str, Any]:
    return load_compatibility_validation_result_json(path)

def validate_context_validation_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []
    if "compatibility" not in payloads:
        errors.append("Missing compatibility artifact")
    if "diagnostics" not in payloads:
        errors.append("Missing diagnostics artifact")
    if "profiles" not in payloads:
        errors.append("Missing profiles artifact")
    if "gate" not in payloads:
        errors.append("Missing gate artifact")
    return errors

def context_validation_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "compatibility_present": "compatibility" in payloads,
        "diagnostics_count": len(payloads.get("diagnostics", [])),
        "profiles_count": len(payloads.get("profiles", [])),
        "gate_present": "gate" in payloads
    }

def context_validation_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    summ = context_validation_artifact_loader_summary(payloads)
    text = f"Artifact Loader Summary: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
