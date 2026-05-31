from typing import Any, Dict, List
from pathlib import Path
import json

from usa_signal_bot.core.exceptions import MonitoringArtifactLoaderError

def _safe_load_json(path: Path) -> Dict[str, Any]:
    if ".." in str(path) or not path.exists():
        raise MonitoringArtifactLoaderError(f"Invalid or missing path: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _safe_load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if ".." in str(path) or not path.exists():
        raise MonitoringArtifactLoaderError(f"Invalid or missing path: {path}")
    res = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_monitoring_baseline_json(path: Path) -> Dict[str, Any]:
    return _safe_load_json(path)

def load_monitoring_snapshot_json(path: Path) -> Dict[str, Any]:
    return _safe_load_json(path)

def load_drift_tracking_result_json(path: Path) -> Dict[str, Any]:
    return _safe_load_json(path)

def load_context_degradation_diagnostics_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _safe_load_jsonl(path)

def load_context_degradation_profiles_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _safe_load_jsonl(path)

def load_monitoring_readiness_gate_json(path: Path) -> Dict[str, Any]:
    return _safe_load_json(path)

def validate_monitoring_artifacts(payloads: Dict[str, Any]) -> List[str]:
    # perform unsafe field / language scans
    from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_safety_validator import FORBIDDEN_FRAGMENTS
    errors = []

    payload_str = json.dumps(payloads).lower()
    for frag in FORBIDDEN_FRAGMENTS:
        if frag in payload_str and frag != "signal":
            errors.append(f"Unsafe artifact content detected: {frag}")

    return errors

def monitoring_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {"keys": list(payloads.keys())}

def monitoring_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    return f"Artifacts: {list(payloads.keys())}"[:limit]
