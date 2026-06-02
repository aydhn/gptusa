import json
import csv
from pathlib import Path
from typing import Any
import pandas as pd

from usa_signal_bot.core.exceptions import DriftMonitoringArtifactLoaderError

def check_unsafe_fields(payload: dict[str, Any], path: Path) -> list[str]:
    errors = []
    unsafe_keys = [
        "live_monitoring_enabled",
        "alert_sender_enabled",
        "live_inference_enabled",
        "online_inference_enabled",
        "broker_execution_enabled",
        "deployment_allowed",
        "active_paper_enabled",
        "strategy_activation_allowed",
        "scheduler_enabled",
        "daemon_started",
        "backtest_executed"
    ]
    for key in unsafe_keys:
        if payload.get(key, False):
            errors.append(f"Unsafe field {key}=True in {path}")
    return errors

def load_monitoring_metadata_package_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def load_post_ensemble_governance_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def load_non_activation_drift_boundary_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def load_drift_readiness_gate_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def load_model_card_drift_updates_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    data = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def load_feature_matrix_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    return pd.read_csv(path)

def load_factor_matrix_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    return pd.read_csv(path)

def load_phase_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DriftMonitoringArtifactLoaderError(f"File not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def validate_drift_monitoring_artifacts(payloads: dict[str, Any]) -> list[str]:
    errors = []
    for name, payload in payloads.items():
        if isinstance(payload, dict):
            errors.extend(check_unsafe_fields(payload, Path(name)))
        elif isinstance(payload, list):
            for i, item in enumerate(payload):
                if isinstance(item, dict):
                    errors.extend(check_unsafe_fields(item, Path(f"{name}[{i}]")))
    return errors

def drift_monitoring_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    return {
        "loaded_artifacts": list(payloads.keys()),
        "count": len(payloads)
    }

def drift_monitoring_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 300) -> str:
    summary = drift_monitoring_artifact_loader_summary(payloads)
    return f"Loaded {summary['count']} artifacts: {', '.join(summary['loaded_artifacts'])}"
