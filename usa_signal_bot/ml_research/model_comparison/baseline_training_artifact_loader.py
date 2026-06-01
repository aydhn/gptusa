import json
from pathlib import Path
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    ModelComparisonInputReference,
    create_model_comparison_input_reference_id
)

def load_non_activation_model_registry_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_offline_evaluation_reports_jsonl(path: Path) -> list[dict[str, Any]]:
    reports = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                reports.append(json.loads(line))
    return reports

def load_offline_prediction_artifacts_jsonl(path: Path) -> list[dict[str, Any]]:
    artifacts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                artifacts.append(json.loads(line))
    return artifacts

def load_fitted_model_artifacts_jsonl(path: Path) -> list[dict[str, Any]]:
    artifacts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                artifacts.append(json.loads(line))
    return artifacts

def load_model_card_updates_jsonl(path: Path) -> list[dict[str, Any]]:
    updates = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                updates.append(json.loads(line))
    return updates

def validate_baseline_training_artifacts(payloads: dict[str, Any]) -> list[str]:
    # Dummy implementation for blocking checks
    errors = []
    for key, val in payloads.items():
        val_str = str(val).lower()
        if "buy" in val_str or "sell" in val_str or "live" in val_str:
            if key != 'prediction_artifacts': # naive exclusions
                 errors.append(f"Forbidden term found in artifact {key}")
    return errors

def build_model_comparison_input_references(payloads: dict[str, Any]) -> list[ModelComparisonInputReference]:
    refs = []
    for k, v in payloads.items():
        refs.append(
            ModelComparisonInputReference(
                reference_id=create_model_comparison_input_reference_id(),
                created_at_utc="now",
                input_kind="UNKNOWN",
                artifact_name=k,
                source_path=None,
                source_hash=None,
                source_id=None,
                experiment_id=None,
                model_artifact_id=None,
                available=True,
                read_only=True,
                research_data_only=True,
                offline_ml_research_only=True,
                contains_trade_signal=False,
                contains_order_decision=False,
                contains_portfolio_weight=False,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
        )
    return refs

def baseline_training_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    return {"loaded_keys": list(payloads.keys())}

def baseline_training_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 300) -> str:
    return str(list(payloads.keys()))[:limit]
