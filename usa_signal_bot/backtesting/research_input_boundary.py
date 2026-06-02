from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestResearchInputContract,
    create_backtest_research_input_contract_id
)
from usa_signal_bot.core.enums import BacktestFoundationRiskFlag

FORBIDDEN_ACTIVE_COLUMNS = [
    "buy_signal", "sell_signal", "entry", "exit", "order", "broker_order",
    "paper_order", "live_order", "position", "portfolio_weight",
    "target_weight", "allocation", "sent_to_broker", "strategy_active",
    "deployment_enabled"
]

def build_backtest_research_input_contract() -> BacktestResearchInputContract:
    return BacktestResearchInputContract(
        contract_id=create_backtest_research_input_contract_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        allowed_research_columns=["prediction", "score", "probability", "rank", "regime"],
        forbidden_active_trading_columns=FORBIDDEN_ACTIVE_COLUMNS,
        signal_activation_allowed=False,
        order_decision_allowed=False,
        paper_mutation_allowed=False,
        portfolio_allocation_allowed=False,
        strategy_activation_allowed=False,
        contract_valid=True,
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_backtest_research_input_contract(contract: BacktestResearchInputContract) -> list[str]:
    errors = []
    if contract.signal_activation_allowed:
        errors.append("signal_activation_allowed must be False")
    if contract.order_decision_allowed:
        errors.append("order_decision_allowed must be False")
    if contract.paper_mutation_allowed:
        errors.append("paper_mutation_allowed must be False")
    if contract.portfolio_allocation_allowed:
        errors.append("portfolio_allocation_allowed must be False")
    if contract.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be False")
    return errors

def validate_research_input_columns(columns: list[str]) -> list[str]:
    forbidden = [c for c in columns if c.lower() in FORBIDDEN_ACTIVE_COLUMNS]
    if forbidden:
        return [f"Forbidden active trading columns detected: {forbidden}"]
    return []

def research_input_boundary_summary(contract: BacktestResearchInputContract) -> dict[str, Any]:
    return {"valid": contract.contract_valid, "forbidden_count": len(contract.forbidden_active_trading_columns)}

def research_input_boundary_to_text(contract: BacktestResearchInputContract, limit: int = 300) -> str:
    return f"ResearchInputContract(valid={contract.contract_valid}, signal_activation_allowed={contract.signal_activation_allowed})"
