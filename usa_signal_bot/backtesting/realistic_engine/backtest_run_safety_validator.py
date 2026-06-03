from typing import Dict, Any, List
import pandas as pd
from .phase147_models import (
    BacktestRunContext, BacktestRunArtifact, SimulatedFillRecord,
    BacktestLedger, BasicPerformanceSummary, BacktestRunSafetyBoundaryResult,
    BacktestRunValidationGate, BacktestRunRiskFlag
)

def validate_backtest_run_context_safety(context: BacktestRunContext) -> List[str]:
    errors = []
    if context.live_trading_enabled: errors.append("Live trading enabled in context")
    return errors

def validate_backtest_run_artifact_safety(item: BacktestRunArtifact) -> List[str]:
    errors = []
    if item.broker_execution_enabled: errors.append("Broker execution enabled in artifact")
    return errors

def validate_simulated_fills_safety(items: List[SimulatedFillRecord]) -> List[str]:
    errors = []
    for i in items:
        if i.real_order_created: errors.append(f"Real order created for fill {i.fill_id}")
    return errors

def validate_backtest_ledger_safety(ledger: BacktestLedger) -> List[str]:
    errors = []
    if ledger.paper_state_mutated: errors.append("Paper state mutated in ledger")
    return errors

def validate_basic_performance_safety(summary: BasicPerformanceSummary) -> List[str]:
    errors = []
    if not summary.not_investment_advice: errors.append("Summary is marked as investment advice")
    return errors

def validate_backtest_run_boundary_safety(result: BacktestRunSafetyBoundaryResult) -> List[str]:
    return []

def validate_backtest_run_validation_gate_safety(gate: BacktestRunValidationGate) -> List[str]:
    return []

def validate_backtest_run_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return []

def backtest_run_text_has_trade_or_execution_language(text: str) -> bool:
    unsafe = ["buy ", "sell ", "broker execution", "live deployment", "active strategy"]
    t = text.lower()
    for u in unsafe:
        if u in t: return True
    return False

def collect_backtest_run_risk_flags(context: BacktestRunContext | None = None) -> List[BacktestRunRiskFlag]:
    return []

def backtest_run_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safety_errors": len(errors)}

def backtest_run_safety_to_text(errors: List[str]) -> str:
    return f"Safety errors: {len(errors)}"
