from typing import Any, Dict, Optional, Tuple
from usa_signal_bot.core.enums import RiskThrottleLevel, SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id

def calculate_drawdown_pct(equity_curve: Optional[list[float]] = None, current_equity: Optional[float] = None, peak_equity: Optional[float] = None) -> Optional[float]:
    if equity_curve and len(equity_curve) > 0:
        curr = equity_curve[-1]
        peak = max(equity_curve)
        if peak > 0:
            return ((peak - curr) / peak) * 100.0

    if current_equity is not None and peak_equity is not None and peak_equity > 0:
        return ((peak_equity - current_equity) / peak_equity) * 100.0

    return 0.0

def classify_risk_throttle_level(drawdown_pct: Optional[float]) -> RiskThrottleLevel:
    if drawdown_pct is None or drawdown_pct <= 0:
        return RiskThrottleLevel.NONE

    if drawdown_pct <= 3.0:
        return RiskThrottleLevel.NONE
    elif drawdown_pct <= 6.0:
        return RiskThrottleLevel.LIGHT
    elif drawdown_pct <= 10.0:
        return RiskThrottleLevel.MODERATE
    elif drawdown_pct <= 15.0:
        return RiskThrottleLevel.HEAVY
    else:
        return RiskThrottleLevel.FULL_BLOCK

def drawdown_risk_multiplier(drawdown_pct: Optional[float]) -> float:
    level = classify_risk_throttle_level(drawdown_pct)
    if level == RiskThrottleLevel.NONE:
        return 1.0
    elif level == RiskThrottleLevel.LIGHT:
        return 0.75
    elif level == RiskThrottleLevel.MODERATE:
        return 0.50
    elif level == RiskThrottleLevel.HEAVY:
        return 0.25
    elif level == RiskThrottleLevel.FULL_BLOCK:
        return 0.0
    return 1.0

def apply_drawdown_throttle(notional_usd: Optional[float], drawdown_pct: Optional[float]) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    multiplier = drawdown_risk_multiplier(drawdown_pct)
    if multiplier < 1.0:
        adjusted = notional_usd * multiplier
        level = classify_risk_throttle_level(drawdown_pct)
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.DRAWDOWN_THROTTLE),
            reason=SizingAdjustmentReason.DRAWDOWN_THROTTLE,
            multiplier=multiplier,
            delta_notional_usd=adjusted - notional_usd,
            description=f"Drawdown throttle applied at {level.value} level."
        )
        return adjusted, adj

    return notional_usd, None

def drawdown_throttle_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Drawdown Pct: {payload.get('drawdown_pct', 'N/A')}\n"
        f"Throttle Level: {payload.get('throttle_level', 'N/A')}\n"
        f"Throttle Multiplier: {payload.get('multiplier', 'N/A')}\n"
    )
