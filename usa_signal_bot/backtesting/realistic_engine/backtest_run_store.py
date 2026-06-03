import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from .phase147_models import (
    BacktestRunContext, BacktestRunFullReview, BacktestRunConfig,
    ResearchDecisionStream, PriceEventStream, SimulatedFillRecord,
    CostLedgerRecord, ExposureStateRecord, EquityCurvePoint, DrawdownPoint,
    BasicPerformanceSummary, BacktestRunArtifact, BacktestRunSafetyBoundaryResult,
    BacktestRunValidationGate
)

def backtest_run_store_dir(data_root: Path) -> Path: return data_root / "backtesting/runs"
def backtest_run_contexts_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "contexts"
def backtest_run_reviews_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "reviews"
def backtest_run_configs_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "configs"
def research_decision_streams_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "research_decisions"
def price_event_streams_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "price_events"
def simulated_fill_ledgers_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "simulated_fills"
def cost_ledgers_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "cost_ledgers"
def exposure_timelines_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "exposure_timelines"
def equity_curves_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "equity_curves"
def drawdown_curves_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "drawdown_curves"
def performance_summaries_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "performance_summaries"
def run_artifacts_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "artifacts"
def safety_boundaries_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "safety_boundaries"
def validation_gates_dir(data_root: Path) -> Path: return backtest_run_store_dir(data_root) / "validation_gates"

def _ensure_dir(path: Path): path.parent.mkdir(parents=True, exist_ok=True)

def write_backtest_run_context_json(path: Path, item: BacktestRunContext) -> Path:
    _ensure_dir(path)
    return path
def write_backtest_run_full_review_json(path: Path, item: BacktestRunFullReview) -> Path:
    _ensure_dir(path)
    with open(path, "w") as f: json.dump({"review_id": item.review_id}, f)
    return path
def write_backtest_run_config_json(path: Path, item: BacktestRunConfig) -> Path:
    _ensure_dir(path)
    return path
def write_research_decision_stream_csv(path: Path, item: ResearchDecisionStream) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in item.records]).to_csv(path, index=False)
    return path
def write_price_event_stream_csv(path: Path, item: PriceEventStream) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in item.events]).to_csv(path, index=False)
    return path
def write_simulated_fill_ledger_csv(path: Path, items: List[SimulatedFillRecord]) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in items]).to_csv(path, index=False)
    return path
def write_cost_ledger_csv(path: Path, items: List[CostLedgerRecord]) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in items]).to_csv(path, index=False)
    return path
def write_exposure_timeline_csv(path: Path, items: List[ExposureStateRecord]) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in items]).to_csv(path, index=False)
    return path
def write_equity_curve_csv(path: Path, items: List[EquityCurvePoint]) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in items]).to_csv(path, index=False)
    return path
def write_drawdown_curve_csv(path: Path, items: List[DrawdownPoint]) -> Path:
    _ensure_dir(path)
    pd.DataFrame([r.__dict__ for r in items]).to_csv(path, index=False)
    return path
def write_basic_performance_summary_json(path: Path, item: BasicPerformanceSummary) -> Path:
    _ensure_dir(path)
    return path
def write_backtest_run_artifact_json(path: Path, item: BacktestRunArtifact) -> Path:
    _ensure_dir(path)
    return path
def write_backtest_run_safety_boundary_json(path: Path, item: BacktestRunSafetyBoundaryResult) -> Path:
    _ensure_dir(path)
    return path
def write_backtest_run_validation_gate_json(path: Path, item: BacktestRunValidationGate) -> Path:
    _ensure_dir(path)
    return path

def read_backtest_run_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f: return json.load(f)

def list_backtest_run_reviews(data_root: Path) -> List[Path]:
    return []

def get_latest_backtest_run_review(data_root: Path) -> Path | None:
    return None

def backtest_run_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"base_dir": str(backtest_run_store_dir(data_root))}
