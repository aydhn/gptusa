from typing import Optional, Dict, Any, List
from usa_signal_bot.core.enums import CostLiquidityRegime

def classify_cost_liquidity_regime(avg_dollar_volume: Optional[float] = None, avg_daily_volume: Optional[float] = None, liquidity_status: Optional[Any] = None) -> CostLiquidityRegime:
    if str(liquidity_status).upper() in ("FROZEN", "HALTED", "SUSPENDED"):
        return CostLiquidityRegime.FROZEN

    if avg_dollar_volume is None and avg_daily_volume is None:
        return CostLiquidityRegime.INSUFFICIENT_DATA

    adv = avg_dollar_volume if avg_dollar_volume is not None else (avg_daily_volume or 0.0)

    if adv > 100_000_000:
        return CostLiquidityRegime.DEEP
    elif adv >= 10_000_000:
        return CostLiquidityRegime.NORMAL
    elif adv >= 2_000_000:
        return CostLiquidityRegime.THIN
    else:
        return CostLiquidityRegime.ILLIQUID

def liquidity_cost_multiplier(regime: CostLiquidityRegime) -> float:
    mapping = {
        CostLiquidityRegime.DEEP: 0.80,
        CostLiquidityRegime.NORMAL: 1.00,
        CostLiquidityRegime.THIN: 1.75,
        CostLiquidityRegime.ILLIQUID: 3.00,
        CostLiquidityRegime.FROZEN: 5.00,
        CostLiquidityRegime.INSUFFICIENT_DATA: 1.50,
        CostLiquidityRegime.UNKNOWN: 1.50,
    }
    return mapping.get(regime, 1.50)

def liquidity_cost_warnings(regime: CostLiquidityRegime, evidence: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if regime == CostLiquidityRegime.ILLIQUID:
        warnings.append("Illiquid regime. High execution risk.")
    elif regime == CostLiquidityRegime.FROZEN:
        warnings.append("Frozen liquidity detected. Trades may be blocked.")
    elif regime == CostLiquidityRegime.INSUFFICIENT_DATA:
        warnings.append("Insufficient liquidity data. Using conservative costs.")
    return warnings

def liquidity_regime_to_text(regime: CostLiquidityRegime, multiplier: Optional[float] = None) -> str:
    mult_text = f" (Multiplier: {multiplier:.2f})" if multiplier is not None else ""
    return f"Liquidity Regime: {regime.value}{mult_text}"
