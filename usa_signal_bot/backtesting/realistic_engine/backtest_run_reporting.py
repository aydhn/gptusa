from typing import Dict, Any
from .phase147_models import (
    BacktestFoundationIngestionResult, BacktestRunConfig, ResearchDecisionStream,
    SimulationClock, PriceEventStream, SimulatedFillRecord, CostLedgerRecord,
    ExposureStateRecord, BasicPerformanceSummary, BacktestLedger,
    BacktestRunArtifact, BacktestRunSafetyBoundaryResult, BacktestRunValidationGate,
    BacktestRunContext, BacktestRunFullReview
)

def backtest_foundation_ingestion_result_to_text(item: BacktestFoundationIngestionResult) -> str: return str(item)
def backtest_run_config_to_text(item: BacktestRunConfig, limit: int = 300) -> str: return str(item)
def research_decision_stream_to_text(item: ResearchDecisionStream, limit: int = 300) -> str: return str(item)
def simulation_clock_to_text(item: SimulationClock, limit: int = 300) -> str: return str(item)
def price_event_stream_to_text(item: PriceEventStream, limit: int = 300) -> str: return str(item)
def simulated_fill_to_text(item: SimulatedFillRecord) -> str: return str(item)
def cost_ledger_record_to_text(item: CostLedgerRecord) -> str: return str(item)
def exposure_state_to_text(item: ExposureStateRecord) -> str: return str(item)
def basic_performance_summary_to_text(item: BasicPerformanceSummary, limit: int = 300) -> str: return str(item)
def backtest_ledger_to_text(item: BacktestLedger, limit: int = 300) -> str: return str(item)
def backtest_run_artifact_to_text(item: BacktestRunArtifact, limit: int = 300) -> str: return str(item)
def backtest_run_safety_boundary_to_text(item: BacktestRunSafetyBoundaryResult, limit: int = 300) -> str: return str(item)
def backtest_run_validation_gate_to_text(item: BacktestRunValidationGate, limit: int = 300) -> str: return str(item)
def backtest_run_context_to_text(item: BacktestRunContext, limit: int = 300) -> str: return str(item)
def backtest_run_full_review_to_text(item: BacktestRunFullReview, limit: int = 300) -> str: return str(item)
def backtest_run_store_summary_to_text(summary: Dict[str, Any]) -> str: return str(summary)
def backtest_run_limitations_text() -> str: return "Offline deterministic backtest only. No live trading."
