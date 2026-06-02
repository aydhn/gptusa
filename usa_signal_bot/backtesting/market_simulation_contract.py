from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    MarketSimulationContract,
    BacktestDatasetContract,
    BacktestEventTimelineContract,
    ExecutionAssumptionContract,
    TransactionCostModel,
    CommissionModel,
    SpreadModel,
    SlippageModel,
    LiquidityGuard,
    PartialFillAssumption,
    ExecutionLatencyAssumption,
    create_market_simulation_contract_id
)
from usa_signal_bot.core.enums import MarketSimulationContractKind

def build_market_simulation_contract(
    dataset_contract: BacktestDatasetContract,
    timeline: BacktestEventTimelineContract,
    execution: ExecutionAssumptionContract,
    transaction_cost: TransactionCostModel,
    commission: CommissionModel,
    spread: SpreadModel,
    slippage: SlippageModel,
    liquidity: LiquidityGuard,
    partial_fill: PartialFillAssumption,
    latency: ExecutionLatencyAssumption
) -> MarketSimulationContract:

    valid = all([
        dataset_contract.contract_valid,
        timeline.timeline_valid,
        execution.assumption_valid,
        transaction_cost.cost_model_valid,
        commission.commission_model_valid,
        spread.spread_model_valid,
        slippage.slippage_model_valid,
        liquidity.guard_valid,
        partial_fill.assumption_valid,
        latency.assumption_valid
    ])

    return MarketSimulationContract(
        contract_id=create_market_simulation_contract_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        simulation_kind=MarketSimulationContractKind.DAILY_BAR_RESEARCH_SIMULATION,
        dataset_contract_id=dataset_contract.contract_id,
        event_timeline_id=timeline.timeline_id,
        execution_assumption_id=execution.assumption_id,
        transaction_cost_model_id=transaction_cost.model_id,
        commission_model_id=commission.model_id,
        spread_model_id=spread.model_id,
        slippage_model_id=slippage.model_id,
        liquidity_guard_id=liquidity.guard_id,
        partial_fill_assumption_id=partial_fill.assumption_id,
        execution_latency_assumption_id=latency.assumption_id,
        supports_adjusted_prices=dataset_contract.adjusted_price_required,
        supports_corporate_actions=dataset_contract.corporate_actions_supported,
        supports_market_calendar=dataset_contract.market_calendar_supported,
        allows_live_execution=False,
        allows_order_creation=False,
        allows_paper_mutation=False,
        simulation_contract_valid=valid,
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_market_simulation_contract(contract: MarketSimulationContract) -> list[str]:
    errors = []
    if contract.allows_live_execution:
        errors.append("allows_live_execution must be False")
    if contract.allows_order_creation:
        errors.append("allows_order_creation must be False")
    if contract.allows_paper_mutation:
        errors.append("allows_paper_mutation must be False")
    if not contract.simulation_contract_valid:
        errors.append("simulation_contract_valid is False")
    return errors

def market_simulation_contract_summary(contract: MarketSimulationContract) -> dict[str, Any]:
    return {"valid": contract.simulation_contract_valid, "kind": contract.simulation_kind.value}

def market_simulation_contract_to_text(contract: MarketSimulationContract, limit: int = 300) -> str:
    return f"MarketSimulationContract(valid={contract.simulation_contract_valid}, live_exec={contract.allows_live_execution})"
