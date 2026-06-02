from typing import Any
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestFoundationContext,
    BacktestInputReference,
    BacktestDatasetContract,
    BacktestResearchInputContract,
    MarketSimulationContract,
    TransactionCostModel,
    CommissionModel,
    SpreadModel,
    SlippageModel,
    LiquidityGuard,
    BacktestSafetyBoundaryResult,
    BacktestReadinessGate
)
from usa_signal_bot.core.enums import BacktestFoundationRiskFlag

UNSAFE_TERMS = [
    "broker_order", "live_trade", "execute_now", "send_to_telegram", "start_daemon", "guaranteed_return", "investment_advice"
]

def backtest_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in UNSAFE_TERMS)

def validate_backtest_dataframe_output_safety(df: Any) -> list[str]:
    from usa_signal_bot.backtesting.backtest_input_resolver import detect_forbidden_backtest_columns
    errors = []
    cols = list(df.columns)
    forbidden = detect_forbidden_backtest_columns(cols)
    if forbidden:
        errors.append(f"Forbidden columns found in DF: {forbidden}")
    return errors

def validate_backtest_inputs_safety(items: list[BacktestInputReference]) -> list[str]:
    errors = []
    for item in items:
        if item.forbidden_columns_detected:
            errors.append(f"Forbidden columns in input {item.input_kind.value}: {item.forbidden_columns_detected}")
        if not item.research_data_only:
            errors.append(f"Input {item.input_kind.value} must be research_data_only")
    return errors

def validate_backtest_contracts_safety(
    dataset_contract: BacktestDatasetContract,
    research_contract: BacktestResearchInputContract,
    market_contract: MarketSimulationContract
) -> list[str]:
    errors = []
    if not dataset_contract.research_data_only:
        errors.append("Dataset contract must be research_data_only")
    if research_contract.signal_activation_allowed:
        errors.append("Research contract signal_activation_allowed must be False")
    if market_contract.allows_live_execution:
        errors.append("Market contract allows_live_execution must be False")
    return errors

def validate_execution_models_safety(
    transaction_cost: TransactionCostModel,
    commission: CommissionModel,
    spread: SpreadModel,
    slippage: SlippageModel,
    liquidity: LiquidityGuard
) -> list[str]:
    errors = []
    if transaction_cost.live_broker_fee_sync_enabled:
        errors.append("Transaction cost live_broker_fee_sync_enabled must be False")
    if commission.live_broker_fee_sync_enabled:
        errors.append("Commission live_broker_fee_sync_enabled must be False")
    if spread.live_quote_required:
        errors.append("Spread live_quote_required must be False")
    if slippage.live_quote_required:
        errors.append("Slippage live_quote_required must be False")
    if liquidity.order_creation_allowed:
        errors.append("Liquidity order_creation_allowed must be False")
    return errors

def validate_backtest_safety_boundary_safety(result: BacktestSafetyBoundaryResult) -> list[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary passed is False")
    if not result.no_live_trading:
        errors.append("Safety boundary no_live_trading is False")
    if not result.no_full_backtest_run_phase146:
        errors.append("Safety boundary no_full_backtest_run_phase146 is False")
    return errors

def validate_backtest_readiness_gate_safety(gate: BacktestReadinessGate) -> list[str]:
    errors = []
    if gate.live_trading_enabled:
        errors.append("Readiness gate live_trading_enabled is True")
    if gate.full_backtest_run_executed:
        errors.append("Readiness gate full_backtest_run_executed is True")
    return errors

def validate_backtest_foundation_context_safety(context: BacktestFoundationContext) -> list[str]:
    errors = []
    errors.extend(validate_backtest_inputs_safety(context.input_references))
    errors.extend(validate_backtest_contracts_safety(context.dataset_contract, context.research_input_contract, context.market_simulation_contract))
    errors.extend(validate_execution_models_safety(
        context.transaction_cost_model, context.commission_model, context.spread_model, context.slippage_model, context.liquidity_guard
    ))
    errors.extend(validate_backtest_safety_boundary_safety(context.safety_boundary))
    errors.extend(validate_backtest_readiness_gate_safety(context.readiness_gate))

    # Check context direct flags
    if context.live_trading_enabled: errors.append("live_trading_enabled is True")
    if context.paper_trading_enabled: errors.append("paper_trading_enabled is True")
    if context.broker_execution_enabled: errors.append("broker_execution_enabled is True")
    if context.order_creation_enabled: errors.append("order_creation_enabled is True")
    if context.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled is True")
    if context.telegram_real_send_enabled: errors.append("telegram_real_send_enabled is True")
    if context.strategy_activation_allowed: errors.append("strategy_activation_allowed is True")
    if context.portfolio_allocation_allowed: errors.append("portfolio_allocation_allowed is True")
    if context.deployment_allowed: errors.append("deployment_allowed is True")
    if context.network_used: errors.append("network_used is True")
    if context.paid_api_used: errors.append("paid_api_used is True")
    if context.scraping_used: errors.append("scraping_used is True")
    if context.html_parsing_used: errors.append("html_parsing_used is True")
    if context.dashboard_started: errors.append("dashboard_started is True")
    if context.daemon_started: errors.append("daemon_started is True")
    if context.scheduler_enabled: errors.append("scheduler_enabled is True")
    if context.full_backtest_run_executed: errors.append("full_backtest_run_executed is True")
    if context.walk_forward_executed: errors.append("walk_forward_executed is True")
    if context.stress_test_executed: errors.append("stress_test_executed is True")
    if context.monte_carlo_executed: errors.append("monte_carlo_executed is True")
    if context.produces_trade_signal: errors.append("produces_trade_signal is True")
    if context.produces_order_decision: errors.append("produces_order_decision is True")
    if context.produces_portfolio_weights: errors.append("produces_portfolio_weights is True")
    if context.investment_advice: errors.append("investment_advice is True")

    return errors

def collect_backtest_foundation_risk_flags(context: BacktestFoundationContext | None = None) -> list[BacktestFoundationRiskFlag]:
    if not context:
        return []
    flags = []
    if context.live_trading_enabled: flags.append(BacktestFoundationRiskFlag.LIVE_TRADING_RISK)
    if context.paper_trading_enabled: flags.append(BacktestFoundationRiskFlag.PAPER_TRADING_RISK)
    if context.full_backtest_run_executed: flags.append(BacktestFoundationRiskFlag.FULL_BACKTEST_RUN_ATTEMPTED)
    return flags

def backtest_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": len(errors)}

def backtest_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safety OK."
    return f"Safety invalid ({len(errors)} errors): {errors[:3]}..."
