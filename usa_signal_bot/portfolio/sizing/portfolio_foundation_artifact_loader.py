import json
import pandas as pd
from pathlib import Path
from typing import Any

def load_portfolio_foundation_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_candidate_universe_contract_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_constraint_catalog_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_risk_budget_contract_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_position_sizing_boundary_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_candidate_metrics_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_risk_budget_inputs_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def validate_portfolio_foundation_artifacts(payloads: dict[str, Any]) -> list[str]:
    errors = []
    # Check for target_weight, allocation, actual_position_size
    forbidden_keys = [
        "target_weight", "allocation", "actual_position_size",
        "order_size", "capital_allocation", "broker_order", "live_order"
    ]
    for name, payload in payloads.items():
        payload_str = str(payload).lower()
        for key in forbidden_keys:
            if key in payload_str:
                errors.append(f"Forbidden key '{key}' found in artifact '{name}'")
    return errors

def portfolio_foundation_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    return {"loaded_artifacts": list(payloads.keys())}

def portfolio_foundation_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 300) -> str:
    summary = portfolio_foundation_artifact_loader_summary(payloads)
    res = f"Loaded {len(summary['loaded_artifacts'])} artifacts: {summary['loaded_artifacts']}"
    return res[:limit]
