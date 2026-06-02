from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    AdvancedMLClosureIngestionResult,
    BacktestInputReference,
    BacktestDatasetContract,
    BacktestResearchInputContract,
    BacktestEventTimelineContract,
    ExecutionAssumptionContract,
    TransactionCostModel,
    CommissionModel,
    SpreadModel,
    SlippageModel,
    LiquidityGuard,
    PartialFillAssumption,
    ExecutionLatencyAssumption,
    MarketSimulationContract,
    BacktestSafetyBoundaryResult,
    BacktestReadinessGate,
    BacktestFoundationContext,
    BacktestFoundationFullReview
)

def advanced_ml_closure_ingestion_result_to_text(item: AdvancedMLClosureIngestionResult) -> str:
    return f"Ingestion(ready={item.ready_for_phase146}, closed={item.phase136_to_145_closed}, valid={item.valid_for_phase146})"

def backtest_input_reference_to_text(item: BacktestInputReference) -> str:
    return f"InputRef(kind={item.input_kind.value}, ok={not item.errors})"

def backtest_dataset_contract_to_text(item: BacktestDatasetContract, limit: int = 300) -> str:
    return f"DatasetContract(valid={item.contract_valid}, required_inputs={len(item.required_inputs)})"

def backtest_research_input_contract_to_text(item: BacktestResearchInputContract, limit: int = 300) -> str:
    return f"ResearchContract(valid={item.contract_valid})"

def backtest_event_timeline_to_text(item: BacktestEventTimelineContract, limit: int = 300) -> str:
    return f"Timeline(valid={item.timeline_valid}, lookahead_safe={item.prevents_lookahead_bias})"

def execution_assumption_to_text(item: ExecutionAssumptionContract, limit: int = 300) -> str:
    return f"ExecutionAssumption(valid={item.assumption_valid}, live={item.allow_live_execution})"

def transaction_cost_model_to_text(item: TransactionCostModel, limit: int = 300) -> str:
    return f"TxCost(valid={item.cost_model_valid}, kind={item.cost_kind.value})"

def commission_model_to_text(item: CommissionModel, limit: int = 300) -> str:
    return f"Commission(valid={item.commission_model_valid})"

def spread_model_to_text(item: SpreadModel, limit: int = 300) -> str:
    return f"Spread(valid={item.spread_model_valid})"

def slippage_model_to_text(item: SlippageModel, limit: int = 300) -> str:
    return f"Slippage(valid={item.slippage_model_valid})"

def liquidity_guard_to_text(item: LiquidityGuard, limit: int = 300) -> str:
    return f"LiquidityGuard(valid={item.guard_valid})"

def partial_fill_assumption_to_text(item: PartialFillAssumption, limit: int = 300) -> str:
    return f"PartialFill(valid={item.assumption_valid})"

def execution_latency_assumption_to_text(item: ExecutionLatencyAssumption, limit: int = 300) -> str:
    return f"ExecutionLatency(valid={item.assumption_valid})"

def market_simulation_contract_to_text(item: MarketSimulationContract, limit: int = 300) -> str:
    return f"MarketSim(valid={item.simulation_contract_valid})"

def backtest_safety_boundary_to_text(item: BacktestSafetyBoundaryResult, limit: int = 300) -> str:
    return f"SafetyBoundary(passed={item.boundary_passed})"

def backtest_readiness_gate_to_text(item: BacktestReadinessGate, limit: int = 300) -> str:
    return f"ReadinessGate(ready={item.ready_for_phase147})"

def backtest_foundation_context_to_text(item: BacktestFoundationContext, limit: int = 300) -> str:
    return f"FoundationContext(decision={item.decision.value}, ready={item.ready_for_phase147})"

def backtest_foundation_full_review_to_text(item: BacktestFoundationFullReview, limit: int = 300) -> str:
    return f"FoundationReview(ready={item.readiness_gate.ready_for_phase147})"

def backtest_foundation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"StoreSummary(reviews={summary.get('reviews', 0)})"

def backtest_foundation_limitations_text() -> str:
    return "Phase 146 is a foundation setup only. It does not perform actual backtesting, paper trading, live execution, or deployment."
