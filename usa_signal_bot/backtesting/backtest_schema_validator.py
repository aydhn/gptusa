from typing import Any
from usa_signal_bot.backtesting.phase146_models import (
    BacktestInputReference,
    BacktestDatasetContract,
    BacktestResearchInputContract,
    BacktestEventTimelineContract,
    MarketSimulationContract,
    BacktestFoundationContext
)

FORBIDDEN_COLUMNS = {
    "buy_signal", "sell_signal", "entry", "exit", "order", "broker_order",
    "paper_order", "live_order", "position", "portfolio_weight",
    "target_weight", "allocation", "sent_to_broker", "strategy_active",
    "deployment_enabled"
}

def validate_backtest_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_backtest_columns(columns)

def validate_no_forbidden_backtest_columns(columns: list[str]) -> list[str]:
    forbidden = [c for c in columns if c.lower() in FORBIDDEN_COLUMNS]
    if forbidden:
        return [f"Forbidden active trading columns detected: {forbidden}"]
    return []

def validate_backtest_input_reference_schema(item: BacktestInputReference) -> list[str]:
    return validate_no_forbidden_backtest_columns(item.columns)

def validate_backtest_dataset_contract_schema(item: BacktestDatasetContract) -> list[str]:
    errors = []
    if not item.time_column:
        errors.append("Dataset contract missing time_column")
    if not item.symbol_column:
        errors.append("Dataset contract missing symbol_column")
    if not item.price_columns:
        errors.append("Dataset contract missing price_columns")
    return errors

def validate_research_input_contract_schema(item: BacktestResearchInputContract) -> list[str]:
    errors = []
    if not item.contract_valid:
        errors.append("Research input contract not valid")
    return errors

def validate_event_timeline_schema(item: BacktestEventTimelineContract) -> list[str]:
    if not item.event_order:
        return ["Event timeline missing event_order"]
    return []

def validate_market_simulation_contract_schema(item: MarketSimulationContract) -> list[str]:
    if not item.simulation_contract_valid:
        return ["Market simulation contract not valid"]
    return []

def validate_backtest_foundation_context_schema(context: BacktestFoundationContext) -> list[str]:
    errors = []
    for ref in context.input_references:
        errors.extend(validate_backtest_input_reference_schema(ref))
    errors.extend(validate_backtest_dataset_contract_schema(context.dataset_contract))
    errors.extend(validate_research_input_contract_schema(context.research_input_contract))
    errors.extend(validate_event_timeline_schema(context.event_timeline))
    errors.extend(validate_market_simulation_contract_schema(context.market_simulation_contract))
    return errors

def backtest_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": len(errors)}

def backtest_schema_to_text(errors: list[str]) -> str:
    if not errors:
        return "Schema valid."
    return f"Schema invalid ({len(errors)} errors): {errors[:3]}..."
