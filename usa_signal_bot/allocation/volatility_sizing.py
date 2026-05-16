from typing import Any, Dict, Optional
from usa_signal_bot.core.enums import SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id, CapitalState, RiskBudget

def volatility_size_multiplier(atr_pct: Optional[float], low_vol_pct: float = 1.0, high_vol_pct: float = 5.0) -> float:
    if atr_pct is None:
        return 0.50 # Conservative default
    if atr_pct >= high_vol_pct:
        return 0.50 # Reduce size for high volatility
    if atr_pct <= low_vol_pct:
        return 1.25 # Modest boost for low volatility
    return 1.0

def estimate_stop_distance_pct(atr_pct: Optional[float], atr_multiplier: float = 2.0, min_stop_pct: float = 1.0, max_stop_pct: float = 12.0) -> Optional[float]:
    if atr_pct is None:
        return None
    stop_dist = atr_pct * atr_multiplier
    return max(min_stop_pct, min(max_stop_pct, stop_dist))

def notional_from_volatility_target(capital_state: CapitalState, budget: RiskBudget, atr_pct: Optional[float], confidence_multiplier: float = 1.0) -> Optional[float]:
    if atr_pct is None:
        return None

    # Simple target: Notional * ATR = Risk
    risk_amount = capital_state.total_equity_usd * (budget.per_trade_risk_budget_pct / 100.0)

    if atr_pct <= 0:
        return None

    base_notional = risk_amount / (atr_pct / 100.0)
    return base_notional * confidence_multiplier

def volatility_sizing_adjustment(atr_pct: Optional[float]) -> SizingAdjustment:
    multiplier = volatility_size_multiplier(atr_pct)
    if atr_pct is not None and atr_pct >= 5.0:
        reason = SizingAdjustmentReason.HIGH_VOLATILITY
        desc = "Reduced size due to high volatility."
    elif atr_pct is not None and atr_pct <= 1.0:
        reason = SizingAdjustmentReason.LOW_VOLATILITY
        desc = "Boosted size due to low volatility."
    else:
        reason = SizingAdjustmentReason.UNKNOWN
        desc = "Standard volatility multiplier."

    return SizingAdjustment(
        adjustment_id=create_sizing_adjustment_id(reason),
        reason=reason,
        multiplier=multiplier,
        delta_notional_usd=None,
        description=desc
    )

def volatility_sizing_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"ATR Pct: {payload.get('atr_pct', 'N/A')}\n"
        f"Volatility Multiplier: {payload.get('multiplier', 'N/A')}\n"
    )
