from typing import Any, Dict, Optional, Tuple
from usa_signal_bot.core.enums import SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id

def symbol_concentration_pct(symbol_exposure_usd: Optional[float], total_equity_usd: Optional[float]) -> Optional[float]:
    if symbol_exposure_usd is None or total_equity_usd is None or total_equity_usd <= 0:
        return None
    return (symbol_exposure_usd / total_equity_usd) * 100.0

def strategy_concentration_pct(strategy_exposure_usd: Optional[float], total_equity_usd: Optional[float]) -> Optional[float]:
    if strategy_exposure_usd is None or total_equity_usd is None or total_equity_usd <= 0:
        return None
    return (strategy_exposure_usd / total_equity_usd) * 100.0

def side_concentration_pct(side_exposure_usd: Optional[float], total_equity_usd: Optional[float]) -> Optional[float]:
    if side_exposure_usd is None or total_equity_usd is None or total_equity_usd <= 0:
        return None
    return (side_exposure_usd / total_equity_usd) * 100.0

def concentration_size_multiplier(concentration_pct: Optional[float], warning_pct: float = 10.0, block_pct: float = 20.0) -> float:
    if concentration_pct is None:
        return 1.0

    if concentration_pct >= block_pct:
        return 0.0
    elif concentration_pct >= warning_pct:
        return 0.50

    return 1.0

def apply_concentration_guard(notional_usd: Optional[float], concentration_payload: Optional[Dict[str, Any]] = None) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None or concentration_payload is None:
        return notional_usd, None

    max_conc = 0.0
    if "symbol_pct" in concentration_payload and concentration_payload["symbol_pct"] is not None:
        max_conc = max(max_conc, concentration_payload["symbol_pct"])
    if "strategy_pct" in concentration_payload and concentration_payload["strategy_pct"] is not None:
        max_conc = max(max_conc, concentration_payload["strategy_pct"])
    if "side_pct" in concentration_payload and concentration_payload["side_pct"] is not None:
        max_conc = max(max_conc, concentration_payload["side_pct"])

    multiplier = concentration_size_multiplier(max_conc)

    if multiplier < 1.0:
        adjusted = notional_usd * multiplier
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.CONCENTRATION_LIMIT),
            reason=SizingAdjustmentReason.CONCENTRATION_LIMIT,
            multiplier=multiplier,
            delta_notional_usd=adjusted - notional_usd,
            description=f"Reduced size due to concentration level of {max_conc:.2f}%."
        )
        return adjusted, adj

    return notional_usd, None

def concentration_guard_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Max Concentration Pct: {payload.get('max_concentration_pct', 'N/A')}\n"
        f"Concentration Multiplier: {payload.get('multiplier', 'N/A')}\n"
    )
