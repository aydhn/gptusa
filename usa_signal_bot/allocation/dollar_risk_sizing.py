from typing import Any, Dict, Optional, Tuple
from usa_signal_bot.allocation.allocation_models import CapitalState, RiskBudget

def calculate_dollar_risk_amount(capital_state: CapitalState, risk_pct_equity: float) -> float:
    return capital_state.total_equity_usd * (risk_pct_equity / 100.0)

def calculate_quantity_from_dollar_risk(risk_amount_usd: float, reference_price: Optional[float], stop_distance_pct: Optional[float]) -> Optional[float]:
    if reference_price is None or reference_price <= 0:
        return None
    if stop_distance_pct is None or stop_distance_pct <= 0:
        return None

    risk_per_share = reference_price * (stop_distance_pct / 100.0)
    if risk_per_share <= 0:
        return None

    return risk_amount_usd / risk_per_share

def calculate_notional_from_quantity(quantity: Optional[float], reference_price: Optional[float]) -> Optional[float]:
    if quantity is None or reference_price is None or reference_price <= 0:
        return None
    return quantity * reference_price

def dollar_risk_position_size(capital_state: CapitalState, budget: RiskBudget, reference_price: Optional[float], stop_distance_pct: Optional[float]) -> Tuple[Optional[float], Optional[float]]:
    risk_amount = calculate_dollar_risk_amount(capital_state, budget.per_trade_risk_budget_pct)
    quantity = calculate_quantity_from_dollar_risk(risk_amount, reference_price, stop_distance_pct)
    notional = calculate_notional_from_quantity(quantity, reference_price)
    return quantity, notional

def dollar_risk_sizing_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Dollar Risk Amount: {payload.get('risk_amount_usd', 'N/A')}\n"
        f"Estimated Quantity: {payload.get('estimated_quantity', 'N/A')}\n"
        f"Estimated Notional: {payload.get('estimated_notional', 'N/A')}\n"
    )
