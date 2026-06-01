from typing import Any, Dict, List
from pathlib import Path
import json

def load_calibration_governance_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r") as f:
        return json.load(f)

def load_calibration_diagnostics_reports_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists(): return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip(): res.append(json.loads(line))
    return res

def load_post_training_validations_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists(): return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip(): res.append(json.loads(line))
    return res

def load_calibration_readiness_gate_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r") as f:
        return json.load(f)

def load_offline_prediction_artifacts_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists(): return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip(): res.append(json.loads(line))
    return res

def load_offline_prediction_frame_csv(path: Path) -> Any:
    try:
        import pandas
        if path.exists():
            return pandas.read_csv(path)
    except ImportError:
        pass
    return None

def load_model_card_calibration_updates_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists(): return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip(): res.append(json.loads(line))
    return res

def validate_calibration_diagnostics_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []

    # Check for execution/deployment fields
    for k, v in payloads.items():
        if isinstance(v, dict):
            if v.get('live_inference_enabled'): errors.append(f"live_inference_enabled in {k}")
            if v.get('deployment_allowed'): errors.append(f"deployment_allowed in {k}")
            if v.get('ensemble_fitting_performed'): errors.append(f"ensemble_fitting_performed in {k}")
            if v.get('final_ensemble_prediction_created'): errors.append(f"final_ensemble_prediction_created in {k}")
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    if item.get('live_inference_enabled'): errors.append(f"live_inference_enabled in {k}[{i}]")
                    if item.get('deployment_allowed'): errors.append(f"deployment_allowed in {k}[{i}]")
                    if item.get('ensemble_fitting_performed'): errors.append(f"ensemble_fitting_performed in {k}[{i}]")
                    if item.get('final_ensemble_prediction_created'): errors.append(f"final_ensemble_prediction_created in {k}[{i}]")

    return errors

def calibration_diagnostics_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {"loaded_keys": list(payloads.keys())}

def calibration_diagnostics_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    return f"Artifacts loaded: {list(payloads.keys())}"
