import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Tuple

class ModelComparisonArtifactLoaderError(Exception): pass

def load_model_ranking_table_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f: return json.load(f)

def load_candidate_shortlist_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f: return json.load(f)

def load_calibration_readiness_profiles_jsonl(path: Path) -> List[Dict[str, Any]]:
    with open(path, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def load_selection_governance_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f: return json.load(f)

def load_offline_prediction_artifacts_jsonl(path: Path) -> List[Dict[str, Any]]:
    with open(path, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def load_offline_prediction_frame_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_label_matrix_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_target_matrix_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def validate_model_comparison_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errs = []
    str_payload = json.dumps(payloads).lower()
    if "buy" in str_payload and "signal" in str_payload: errs.append("Forbidden word 'buy' found in payload")
    for key in ["live_inference_enabled", "broker_used", "deployment_allowed", "calibration_fitting_performed"]:
        if str_payload.find(f'"{key}": true') != -1:
            errs.append(f"Forbidden key '{key}' is true")
    return errs

def model_comparison_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {"loaded": len(payloads)}

def model_comparison_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    s = str(payloads)
    return s[:limit] + "..." if len(s) > limit else s
