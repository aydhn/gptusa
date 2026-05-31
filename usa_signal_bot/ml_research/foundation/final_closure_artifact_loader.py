from typing import Any, Dict, List
from pathlib import Path
import json
from ...core.exceptions import FinalClosureArtifactLoaderError

def load_ml_input_contract_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_ml_kickoff_gate_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_final_safety_audit_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_freeze_seal_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def validate_final_closure_artifacts(payloads: Dict[str, Any]) -> List[str]:
    return []

def final_closure_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {"loaded": len(payloads)}

def final_closure_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    return f"Loaded {len(payloads)} artifacts"
