import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.exceptions import ExperimentPlanLoadError

def load_experiment_plan_from_dict(payload: dict[str, Any]) -> dict[str, Any]:
    warnings = validate_loaded_experiment_plan(payload)
    if "warnings" not in payload:
        payload["warnings"] = []
    payload["warnings"].extend(warnings)
    return payload

def load_experiment_plan_from_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ExperimentPlanLoadError(f"Experiment plan file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return load_experiment_plan_from_dict(data)
    except json.JSONDecodeError as e:
        raise ExperimentPlanLoadError(f"Failed to parse experiment plan JSON: {str(e)}")

def load_latest_experiment_plan_from_workflow_store(data_root: Path) -> dict[str, Any] | None:
    # A simplified stub for fetching latest from phase 65.
    # We look in the expected workflow store dir.
    plans_dir = data_root / "research_workflow" / "experiment_plans"
    if not plans_dir.exists():
        return None
    files = sorted(plans_dir.glob("*.json"))
    if not files:
        return None
    try:
        with open(files[-1], "r", encoding="utf-8") as f:
            data = json.load(f)
        return load_experiment_plan_from_dict(data)
    except Exception:
        return None

def validate_loaded_experiment_plan(payload: dict[str, Any]) -> list[str]:
    warnings = []
    if "experiment_id" not in payload:
        warnings.append("Missing experiment_id in loaded plan.")
    if payload.get("allowed_for_auto_execution", False):
        warnings.append("BLOCKED: allowed_for_auto_execution is TRUE. Research Execution explicitly forbids auto execution.")
    return warnings

def experiment_plan_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "experiment_id": payload.get("experiment_id"),
        "hypothesis_id": payload.get("hypothesis_id"),
        "title": payload.get("title", "Untitled Experiment"),
        "warnings": payload.get("warnings", [])
    }

def experiment_plan_to_text(payload: dict[str, Any]) -> str:
    lines = []
    lines.append("--- EXPERIMENT PLAN ---")
    lines.append(f"Experiment ID: {payload.get('experiment_id', 'UNKNOWN')}")
    lines.append(f"Title: {payload.get('title', 'Untitled')}")
    warnings = payload.get('warnings', [])
    if warnings:
        lines.append("Warnings:")
        for w in warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)
