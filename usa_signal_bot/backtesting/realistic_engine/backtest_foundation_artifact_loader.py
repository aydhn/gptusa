import json
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
from usa_signal_bot.core.exceptions import BacktestFoundationIngestionError

def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): raise BacktestFoundationIngestionError(f"Missing {path}")
    with open(path, "r") as f:
        return json.load(f)

def load_backtest_readiness_gate_json(path: Path) -> Dict[str, Any]:
    return _load_json(path)

def load_backtest_safety_boundary_json(path: Path) -> Dict[str, Any]:
    return _load_json(path)

def load_dataset_contract_json(path: Path) -> Dict[str, Any]:
    return _load_json(path)

def load_research_input_contract_json(path: Path) -> Dict[str, Any]:
    return _load_json(path)

def load_market_simulation_contract_json(path: Path) -> Dict[str, Any]:
    return _load_json(path)

def load_price_bars_csv(path: Path) -> pd.DataFrame:
    if not path.exists(): raise BacktestFoundationIngestionError(f"Missing {path}")
    return pd.read_csv(path)

def load_research_predictions_csv(path: Path) -> pd.DataFrame:
    if not path.exists(): raise BacktestFoundationIngestionError(f"Missing {path}")
    return pd.read_csv(path)

def validate_backtest_foundation_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []
    for k, v in payloads.items():
        if isinstance(v, dict):
            if v.get("broker_execution_enabled", False):
                errors.append(f"Broker execution enabled in {k}")
            if v.get("paper_state_mutation_enabled", False):
                errors.append(f"Paper state mutation enabled in {k}")
            if v.get("live_trading_enabled", False):
                errors.append(f"Live trading enabled in {k}")
    return errors

def backtest_foundation_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {"loaded_artifacts": list(payloads.keys())}

def backtest_foundation_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    return f"Loaded {len(payloads)} artifacts: {list(payloads.keys())}"
