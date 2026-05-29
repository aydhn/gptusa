from typing import Any
import json
from pathlib import Path

def load_behavior_profiles_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists(): return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip(): res.append(json.loads(line))
    return res

def load_regime_behavior_summaries_jsonl(path: Path) -> list[dict[str, Any]]:
    return load_behavior_profiles_jsonl(path)

def load_diagnostics_interpretations_jsonl(path: Path) -> list[dict[str, Any]]:
    return load_behavior_profiles_jsonl(path)

def load_behavior_report_json(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r") as f:
        return json.load(f)

def validate_behavior_artifacts(payloads: dict[str, Any]) -> list[str]:
    errors = []
    text_data = json.dumps(payloads).lower()
    for w in ["investment advice", "buy signal", "sell signal", "target weight", "deploy to production"]:
        if w in text_data:
            errors.append(f"Unsafe language '{w}' in behavior artifacts")
    return errors

def behavior_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    return {"keys": list(payloads.keys())}

def behavior_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 200) -> str:
    return f"Behavior artifacts loaded: {list(payloads.keys())}"
