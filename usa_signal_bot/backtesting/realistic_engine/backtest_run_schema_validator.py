from typing import Dict, Any, List
from .phase147_models import (
    BacktestRunConfig, ResearchDecisionStream, PriceEventStream,
    SimulatedFillRecord, CostLedgerRecord, ExposureStateRecord,
    EquityCurvePoint, BacktestRunArtifact, BacktestRunContext
)

def validate_backtest_run_config_schema(item: BacktestRunConfig) -> List[str]: return []
def validate_research_decision_stream_schema(item: ResearchDecisionStream) -> List[str]: return []
def validate_price_event_stream_schema(item: PriceEventStream) -> List[str]: return []
def validate_simulated_fill_schema(item: SimulatedFillRecord) -> List[str]: return []
def validate_cost_ledger_schema(item: CostLedgerRecord) -> List[str]: return []
def validate_exposure_state_schema(item: ExposureStateRecord) -> List[str]: return []
def validate_equity_curve_schema(items: List[EquityCurvePoint]) -> List[str]: return []
def validate_backtest_run_artifact_schema(item: BacktestRunArtifact) -> List[str]: return []
def validate_backtest_run_context_schema(context: BacktestRunContext) -> List[str]: return []

def validate_backtest_run_column_names(columns: List[str]) -> List[str]: return []

def validate_no_forbidden_backtest_run_columns(columns: List[str]) -> List[str]:
    forbidden = ["buy_signal", "sell_signal", "broker_order", "paper_order", "live_order"]
    found = [c for c in columns if c in forbidden]
    return [f"Forbidden column: {c}" for c in found]

def backtest_run_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"schema_errors": len(errors)}

def backtest_run_schema_to_text(errors: List[str]) -> str:
    return f"Schema errors: {len(errors)}"
