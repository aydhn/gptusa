from typing import Any, Dict, Optional, Tuple, List
from usa_signal_bot.core.enums import SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id

def liquidity_size_multiplier(liquidity_payload: Optional[Dict[str, Any]] = None) -> float:
    if liquidity_payload is None:
        return 0.50 # Conservative default

    if liquidity_payload.get("status") in ["BLOCK_SIGNAL", "ILLIQUID"]:
        return 0.0

    if liquidity_payload.get("status") == "THIN":
        return 0.50

    return 1.0

def tradability_size_multiplier(tradability_payload: Optional[Dict[str, Any]] = None) -> float:
    if tradability_payload is None:
        return 1.0

    if not tradability_payload.get("is_tradable", True):
        return 0.0

    return 1.0

def apply_liquidity_size_adjustment(notional_usd: Optional[float], liquidity_payload: Optional[Dict[str, Any]] = None, tradability_payload: Optional[Dict[str, Any]] = None) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    liq_mult = liquidity_size_multiplier(liquidity_payload)
    trad_mult = tradability_size_multiplier(tradability_payload)

    final_mult = min(liq_mult, trad_mult)

    if final_mult < 1.0:
        adjusted_notional = notional_usd * final_mult
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.LOW_LIQUIDITY),
            reason=SizingAdjustmentReason.LOW_LIQUIDITY,
            multiplier=final_mult,
            delta_notional_usd=adjusted_notional - notional_usd,
            description="Reduced size due to low liquidity or tradability constraints."
        )
        return adjusted_notional, adj

    return notional_usd, None

def liquidity_size_warnings(liquidity_payload: Optional[Dict[str, Any]] = None, tradability_payload: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if liquidity_payload is None:
        warnings.append("Liquidity payload missing, using conservative sizing.")
    elif liquidity_payload.get("status") in ["BLOCK_SIGNAL", "ILLIQUID"]:
        warnings.append("Symbol is illiquid. Sizing blocked.")

    if tradability_payload and not tradability_payload.get("is_tradable", True):
        warnings.append("Symbol is marked untradable. Sizing blocked.")

    return warnings

def liquidity_size_adjuster_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Liquidity Multiplier: {payload.get('liquidity_multiplier', 'N/A')}\n"
        f"Tradability Multiplier: {payload.get('tradability_multiplier', 'N/A')}\n"
    )
