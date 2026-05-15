from typing import Optional, Dict, Any, List
from usa_signal_bot.core.enums import CostSpreadRegime

def classify_cost_spread_regime(spread_proxy_bps: Optional[float] = None) -> CostSpreadRegime:
    if spread_proxy_bps is None or spread_proxy_bps < 0:
        return CostSpreadRegime.INSUFFICIENT_DATA

    if spread_proxy_bps > 200.0:
        return CostSpreadRegime.VERY_WIDE
    elif spread_proxy_bps > 80.0:
        return CostSpreadRegime.WIDE
    elif spread_proxy_bps >= 20.0:
        return CostSpreadRegime.NORMAL
    else:
        return CostSpreadRegime.TIGHT

def spread_cost_multiplier(regime: CostSpreadRegime) -> float:
    mapping = {
        CostSpreadRegime.TIGHT: 0.85,
        CostSpreadRegime.NORMAL: 1.00,
        CostSpreadRegime.WIDE: 1.75,
        CostSpreadRegime.VERY_WIDE: 2.75,
        CostSpreadRegime.UNRELIABLE: 3.50,
        CostSpreadRegime.INSUFFICIENT_DATA: 1.25,
        CostSpreadRegime.UNKNOWN: 1.25,
    }
    return mapping.get(regime, 1.25)

def spread_cost_warnings(regime: CostSpreadRegime, evidence: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if regime in (CostSpreadRegime.VERY_WIDE, CostSpreadRegime.UNRELIABLE):
        warnings.append("Very wide or unreliable spreads detected. High slippage likely.")
    elif regime == CostSpreadRegime.INSUFFICIENT_DATA:
        warnings.append("Insufficient spread data.")
    return warnings

def spread_regime_to_text(regime: CostSpreadRegime, multiplier: Optional[float] = None) -> str:
    mult_text = f" (Multiplier: {multiplier:.2f})" if multiplier is not None else ""
    return f"Spread Regime: {regime.value}{mult_text}"
