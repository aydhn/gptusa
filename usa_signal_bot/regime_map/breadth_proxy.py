from typing import Any
from usa_signal_bot.core.enums import BreadthRegime, TrendRegime, MomentumRegime
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation
from usa_signal_bot.regime_map.trend_confirmation import moving_average

def calculate_breadth_score(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations:
        return None
    ratio = uptrend_ratio(confirmations)
    if ratio is None:
         return None
    return ratio * 100.0

def classify_breadth_regime(confirmations: list[MultiTimeframeRegimeConfirmation]) -> BreadthRegime:
    if not confirmations or len(confirmations) < 5:
        return BreadthRegime.INSUFFICIENT_DATA

    ratio = uptrend_ratio(confirmations)
    if ratio is None:
        return BreadthRegime.INSUFFICIENT_DATA

    mom_ratio = momentum_positive_ratio(confirmations)

    if ratio > 0.70 and mom_ratio and mom_ratio > 0.60:
        return BreadthRegime.BROAD_RISK_ON
    elif ratio > 0.55:
        if mom_ratio and mom_ratio < 0.40:
             return BreadthRegime.DETERIORATING
        return BreadthRegime.RISK_ON
    elif ratio < 0.35:
        return BreadthRegime.RISK_OFF
    elif ratio < 0.50 and mom_ratio and mom_ratio < 0.30:
        return BreadthRegime.DETERIORATING
    else:
        return BreadthRegime.MIXED

def uptrend_ratio(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations:
        return None
    up_trends = [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]
    valid = [c for c in confirmations if c.dominant_trend_regime != TrendRegime.INSUFFICIENT_DATA]
    if not valid:
         return None
    ups = sum(1 for c in valid if c.dominant_trend_regime in up_trends)
    return ups / len(valid)

def above_ma_proxy_ratio(symbol_rows: dict[str, list[dict[str, Any]]], window: int = 50) -> float | None:
    if not symbol_rows:
        return None
    valid = 0
    above = 0
    for sym, rows in symbol_rows.items():
        if len(rows) < window:
            continue
        closes = [r["close"] for r in rows]
        ma = moving_average(closes, window)
        if ma:
            valid += 1
            if closes[-1] > ma:
                above += 1
    if valid == 0:
        return None
    return above / valid

def momentum_positive_ratio(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations:
        return None
    pos = [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE]
    valid = [c for c in confirmations if c.dominant_momentum_regime != MomentumRegime.INSUFFICIENT_DATA]
    if not valid:
        return None
    up_moms = sum(1 for c in valid if c.dominant_momentum_regime in pos)
    return up_moms / len(valid)

def breadth_proxy_summary(confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, Any]:
    return {
        "symbol_count": len(confirmations),
        "breadth_score": calculate_breadth_score(confirmations),
        "regime": classify_breadth_regime(confirmations).value,
        "uptrend_ratio": uptrend_ratio(confirmations),
        "momentum_positive_ratio": momentum_positive_ratio(confirmations)
    }

def breadth_proxy_summary_to_text(summary: dict[str, Any]) -> str:
    return (f"Breadth Proxy Summary:\n"
            f"Regime: {summary['regime']}\n"
            f"Score: {summary.get('breadth_score', 0):.2f}\n"
            f"Symbols: {summary['symbol_count']}")
