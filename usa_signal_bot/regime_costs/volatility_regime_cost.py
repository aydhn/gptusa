from typing import Optional, Dict, Any, List
from usa_signal_bot.core.enums import CostVolatilityRegime

def classify_cost_volatility_regime(atr_pct: Optional[float] = None, gap_pct: Optional[float] = None, realized_vol_pct: Optional[float] = None) -> CostVolatilityRegime:
    if atr_pct is None and gap_pct is None and realized_vol_pct is None:
        return CostVolatilityRegime.INSUFFICIENT_DATA

    val = atr_pct if atr_pct is not None else (realized_vol_pct if realized_vol_pct is not None else 0.0)
    g = gap_pct if gap_pct is not None else 0.0

    if val > 6.0 or g >= 10.0:
        return CostVolatilityRegime.EXTREME
    elif val > 3.0:
        return CostVolatilityRegime.HIGH
    elif val >= 1.0:
        return CostVolatilityRegime.NORMAL
    elif val > 0.5:
        return CostVolatilityRegime.LOW
    else:
        return CostVolatilityRegime.VERY_LOW

def volatility_cost_multiplier(regime: CostVolatilityRegime) -> float:
    mapping = {
        CostVolatilityRegime.VERY_LOW: 0.85,
        CostVolatilityRegime.LOW: 0.95,
        CostVolatilityRegime.NORMAL: 1.00,
        CostVolatilityRegime.HIGH: 1.50,
        CostVolatilityRegime.EXTREME: 2.50,
        CostVolatilityRegime.INSUFFICIENT_DATA: 1.25,
        CostVolatilityRegime.UNKNOWN: 1.25,
    }
    return mapping.get(regime, 1.25)

def volatility_cost_warnings(regime: CostVolatilityRegime, evidence: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if regime == CostVolatilityRegime.EXTREME:
        warnings.append("Extreme volatility detected. Slippage models may underestimate true costs.")
    elif regime == CostVolatilityRegime.INSUFFICIENT_DATA:
        warnings.append("Insufficient data for volatility classification. Using conservative estimates.")
    return warnings

def volatility_regime_to_text(regime: CostVolatilityRegime, multiplier: Optional[float] = None) -> str:
    mult_text = f" (Multiplier: {multiplier:.2f})" if multiplier is not None else ""
    return f"Volatility Regime: {regime.value}{mult_text}"
