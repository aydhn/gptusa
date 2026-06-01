"""Phase 139 Artifact Loader"""
from pathlib import Path
from typing import Any
import json

def load_experiment_registry_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_evaluation_harness_contract_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_prediction_output_boundary_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_non_activation_boundary_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def load_model_card_drafts_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def validate_baseline_scaffolding_artifacts(payloads: dict[str, Any]) -> list[str]:
    errors = []
    if "experiment_registry" not in payloads:
        errors.append("Missing experiment_registry")
    if "evaluation_harness_contract" not in payloads:
        errors.append("Missing evaluation_harness_contract")
    if "prediction_output_boundary" not in payloads:
        errors.append("Missing prediction_output_boundary")
    return errors

def baseline_scaffolding_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    return {"keys": list(payloads.keys())}

def baseline_scaffolding_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 300) -> str:
    return "Loader summary: " + str(list(payloads.keys()))
