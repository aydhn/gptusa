from typing import Any, Dict, Optional, Tuple, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import RiskBudgetStatus
from usa_signal_bot.allocation.allocation_models import RiskBudget, CapitalState, create_risk_budget_id, validate_risk_budget

def default_risk_budget() -> RiskBudget:
    budget = RiskBudget(
        budget_id=create_risk_budget_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        portfolio_risk_budget_pct=10.0,
        per_trade_risk_budget_pct=0.50,
        per_symbol_risk_budget_pct=2.0,
        per_strategy_risk_budget_pct=4.0,
        max_position_notional_pct=10.0,
        max_position_notional_usd=None,
        max_daily_new_risk_pct=3.0,
        status=RiskBudgetStatus.AVAILABLE,
        warnings=[],
        errors=[],
        metadata={"note": "Default risk budget."}
    )
    validate_risk_budget(budget)
    return budget

def build_risk_budget_from_config(config_dict: Optional[Dict[str, Any]] = None) -> RiskBudget:
    if config_dict is None:
        return default_risk_budget()

    budget = RiskBudget(
        budget_id=create_risk_budget_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        portfolio_risk_budget_pct=config_dict.get("portfolio_risk_budget_pct", 10.0),
        per_trade_risk_budget_pct=config_dict.get("per_trade_risk_budget_pct", 0.50),
        per_symbol_risk_budget_pct=config_dict.get("per_symbol_risk_budget_pct", 2.0),
        per_strategy_risk_budget_pct=config_dict.get("per_strategy_risk_budget_pct", 4.0),
        max_position_notional_pct=config_dict.get("max_position_notional_pct", 10.0),
        max_position_notional_usd=config_dict.get("max_position_notional_usd"),
        max_daily_new_risk_pct=config_dict.get("max_daily_new_risk_pct", 3.0),
        status=RiskBudgetStatus.AVAILABLE,
        warnings=[],
        errors=[],
        metadata=config_dict
    )
    validate_risk_budget(budget)
    return budget

def modulate_risk_budget(
    base_budget: RiskBudget,
    regime_payload: Optional[Dict[str, Any]] = None,
    drawdown_payload: Optional[Dict[str, Any]] = None,
    execution_payload: Optional[Dict[str, Any]] = None
) -> RiskBudget:

    new_budget = RiskBudget(
        budget_id=create_risk_budget_id("modulated_budget"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        portfolio_risk_budget_pct=base_budget.portfolio_risk_budget_pct,
        per_trade_risk_budget_pct=base_budget.per_trade_risk_budget_pct,
        per_symbol_risk_budget_pct=base_budget.per_symbol_risk_budget_pct,
        per_strategy_risk_budget_pct=base_budget.per_strategy_risk_budget_pct,
        max_position_notional_pct=base_budget.max_position_notional_pct,
        max_position_notional_usd=base_budget.max_position_notional_usd,
        max_daily_new_risk_pct=base_budget.max_daily_new_risk_pct,
        status=base_budget.status,
        warnings=list(base_budget.warnings),
        errors=list(base_budget.errors),
        metadata=dict(base_budget.metadata)
    )

    if regime_payload and regime_payload.get("high_transition_risk", False):
        new_budget.per_trade_risk_budget_pct *= 0.5
        new_budget.status = RiskBudgetStatus.REDUCED_BY_REGIME
        new_budget.warnings.append("Risk budget reduced due to high transition risk.")

    if drawdown_payload and drawdown_payload.get("drawdown_pct", 0) > 5.0:
        new_budget.per_trade_risk_budget_pct *= 0.5
        new_budget.status = RiskBudgetStatus.REDUCED_BY_DRAWDOWN
        new_budget.warnings.append("Risk budget reduced due to high drawdown.")

    if execution_payload and execution_payload.get("illiquid", False):
        new_budget.per_trade_risk_budget_pct = 0.0
        new_budget.status = RiskBudgetStatus.BLOCKED
        new_budget.warnings.append("Risk budget blocked due to illiquidity.")

    validate_risk_budget(new_budget)
    return new_budget

def risk_budget_available_for_trade(capital_state: CapitalState, budget: RiskBudget, symbol: Optional[str] = None, strategy_name: Optional[str] = None) -> Tuple[bool, List[str]]:
    warnings = []

    if budget.status in [RiskBudgetStatus.EXHAUSTED, RiskBudgetStatus.BLOCKED]:
        warnings.append(f"Risk budget is {budget.status.value}")
        return False, warnings

    if capital_state.available_cash_usd <= 0:
        warnings.append("Available cash is zero or negative.")
        return False, warnings

    return True, warnings

def max_trade_notional_from_budget(capital_state: CapitalState, budget: RiskBudget) -> float:
    max_by_pct = capital_state.total_equity_usd * (budget.max_position_notional_pct / 100.0)
    if budget.max_position_notional_usd is not None:
        return min(max_by_pct, budget.max_position_notional_usd)
    return max_by_pct

def risk_budget_to_text(budget: RiskBudget) -> str:
    text = f"Risk Budget [{budget.budget_id}]\n"
    text += f"Status: {budget.status.value}\n"
    text += f"Per Trade Risk: {budget.per_trade_risk_budget_pct:.2f}%\n"
    text += f"Max Position Notional: {budget.max_position_notional_pct:.2f}%\n"
    if budget.warnings:
        text += f"Warnings: {', '.join(budget.warnings)}\n"
    return text
