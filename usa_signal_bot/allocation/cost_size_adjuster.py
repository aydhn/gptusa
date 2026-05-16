from typing import Any, Dict, Optional, Tuple, List
from usa_signal_bot.core.enums import SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id

def cost_size_multiplier(cost_payload: Optional[Dict[str, Any]] = None, robustness_payload: Optional[Dict[str, Any]] = None) -> float:
    multiplier = 1.0

    if cost_payload:
        total_bps = cost_payload.get("total_cost_bps", 0)
        if total_bps > 50: # High cost threshold
            multiplier = min(multiplier, 0.50)

        impact_level = cost_payload.get("market_impact_level", "NORMAL")
        if impact_level == "EXTREME":
            multiplier = min(multiplier, 0.0)
        elif impact_level == "HIGH":
            multiplier = min(multiplier, 0.50)

    if robustness_payload:
        if not robustness_payload.get("is_robust", True):
            multiplier = min(multiplier, 0.25)

    return multiplier

def apply_cost_size_adjustment(notional_usd: Optional[float], cost_payload: Optional[Dict[str, Any]] = None, robustness_payload: Optional[Dict[str, Any]] = None) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    multiplier = cost_size_multiplier(cost_payload, robustness_payload)

    if multiplier < 1.0:
        adjusted_notional = notional_usd * multiplier
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.HIGH_TRANSACTION_COST),
            reason=SizingAdjustmentReason.HIGH_TRANSACTION_COST,
            multiplier=multiplier,
            delta_notional_usd=adjusted_notional - notional_usd,
            description="Reduced size due to transaction cost or fragility constraints."
        )
        return adjusted_notional, adj

    return notional_usd, None

def cost_size_warnings(cost_payload: Optional[Dict[str, Any]] = None, robustness_payload: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if cost_payload:
        if cost_payload.get("market_impact_level") == "EXTREME":
            warnings.append("Extreme market impact expected.")
    if robustness_payload:
        if not robustness_payload.get("is_robust", True):
            warnings.append("Strategy is cost fragile.")
    return warnings

def cost_size_adjuster_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Cost Multiplier: {payload.get('multiplier', 'N/A')}\n"
    )
