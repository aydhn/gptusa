import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import EnsembleScaffoldingArtifactLoaderError

def load_ensemble_preparation_reports_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_ensemble_governance_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_non_activation_ensemble_boundary_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_ensemble_readiness_gate_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_ensemble_candidates_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_candidate_groups_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_blend_plans_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_offline_prediction_artifacts_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def load_offline_prediction_frame_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

def validate_ensemble_scaffolding_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []
    # Check for live inference / deployment flags in dicts
    for k, v in payloads.items():
        if isinstance(v, dict):
            if v.get("live_inference_enabled") or v.get("deployment_allowed"):
                errors.append(f"Unsafe flags in {k}")
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                     if item.get("live_inference_enabled") or item.get("deployment_allowed"):
                         errors.append(f"Unsafe flags in {k}[{i}]")

    return errors

def ensemble_scaffolding_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {k: len(v) if isinstance(v, list) else 1 for k,v in payloads.items()}

def ensemble_scaffolding_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    return str(ensemble_scaffolding_artifact_loader_summary(payloads))
