import json
from pathlib import Path
from typing import Any
import dataclasses

from usa_signal_bot.backtesting.phase146_models import (
    BacktestFoundationContext,
    BacktestFoundationFullReview,
    BacktestInputReference,
    BacktestDatasetContract,
    BacktestResearchInputContract,
    BacktestEventTimelineContract,
    ExecutionAssumptionContract,
    TransactionCostModel,
    MarketSimulationContract,
    BacktestSafetyBoundaryResult,
    BacktestReadinessGate
)

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        from enum import Enum
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

def backtest_foundation_store_dir(data_root: Path) -> Path:
    d = data_root / "data" / "backtesting" / "foundation"
    d.mkdir(parents=True, exist_ok=True)
    return d

def backtest_foundation_contexts_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def backtest_foundation_reviews_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def backtest_inputs_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "inputs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dataset_contracts_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "dataset_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def research_input_contracts_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "research_input_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_timelines_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "event_timelines"
    d.mkdir(parents=True, exist_ok=True)
    return d

def execution_assumptions_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "execution_assumptions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def cost_models_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "cost_models"
    d.mkdir(parents=True, exist_ok=True)
    return d

def market_simulation_contracts_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "market_simulation_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def safety_boundaries_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "safety_boundaries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def readiness_gates_dir(data_root: Path) -> Path:
    d = backtest_foundation_store_dir(data_root) / "readiness_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, data: Any) -> Path:
    with open(path, "w") as f:
        json.dump(data, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_backtest_foundation_context_json(path: Path, item: BacktestFoundationContext) -> Path:
    return _write_json(path, item)

def write_backtest_foundation_full_review_json(path: Path, item: BacktestFoundationFullReview) -> Path:
    return _write_json(path, item)

def write_backtest_input_refs_jsonl(path: Path, items: list[BacktestInputReference]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclasses.asdict(item), cls=EnhancedJSONEncoder) + "\n")
    return path

def write_backtest_dataset_contract_json(path: Path, item: BacktestDatasetContract) -> Path:
    return _write_json(path, item)

def write_research_input_contract_json(path: Path, item: BacktestResearchInputContract) -> Path:
    return _write_json(path, item)

def write_event_timeline_json(path: Path, item: BacktestEventTimelineContract) -> Path:
    return _write_json(path, item)

def write_execution_assumption_json(path: Path, item: ExecutionAssumptionContract) -> Path:
    return _write_json(path, item)

def write_transaction_cost_model_json(path: Path, item: TransactionCostModel) -> Path:
    return _write_json(path, item)

def write_market_simulation_contract_json(path: Path, item: MarketSimulationContract) -> Path:
    return _write_json(path, item)

def write_backtest_safety_boundary_json(path: Path, item: BacktestSafetyBoundaryResult) -> Path:
    return _write_json(path, item)

def write_backtest_readiness_gate_json(path: Path, item: BacktestReadinessGate) -> Path:
    return _write_json(path, item)

def read_backtest_foundation_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_backtest_foundation_reviews(data_root: Path) -> list[Path]:
    d = backtest_foundation_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime)

def get_latest_backtest_foundation_review(data_root: Path) -> Path | None:
    files = list_backtest_foundation_reviews(data_root)
    if files:
        return files[-1]
    return None

def backtest_foundation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_backtest_foundation_reviews(data_root))
    }
