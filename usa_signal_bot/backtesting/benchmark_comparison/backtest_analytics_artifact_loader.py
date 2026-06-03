import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List

def load_backtest_analytics_report_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_run_validation_report_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_backtest_analytics_safety_boundary_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_phase149_readiness_gate_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def load_strategy_equity_curve_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_strategy_return_series_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_price_bars_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_benchmark_reference_prices_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def validate_backtest_analytics_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []
    forbidden_keys = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "real_order", "live_signal"
    ]

    for key, payload in payloads.items():
        if isinstance(payload, dict):
            for f_key in forbidden_keys:
                if f_key in payload and payload[f_key] is True:
                    errors.append(f"Forbidden execution field '{f_key}' found as True in {key}")

    return errors

def backtest_analytics_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "loaded_artifacts_count": len(payloads),
        "keys": list(payloads.keys())
    }

def backtest_analytics_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    summary = backtest_analytics_artifact_loader_summary(payloads)
    text = f"Loaded {summary['loaded_artifacts_count']} artifacts:\n"
    for key in summary['keys']:
        text += f"- {key}\n"
    return text[:limit]
