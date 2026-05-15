from typing import Any
from usa_signal_bot.core.enums import BreadthRegime, TrendRegime, MomentumRegime
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation

def uptrend_ratio(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations:
        return None

    uptrend_count = sum(1 for c in confirmations if c.dominant_trend_regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND])
    return (uptrend_count / len(confirmations)) * 100

def momentum_positive_ratio(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
     if not confirmations:
        return None

     pos_count = sum(1 for c in confirmations if c.dominant_momentum_regime in [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE])
     return (pos_count / len(confirmations)) * 100

def above_ma_proxy_ratio(symbol_rows: dict[str, list[dict[str, Any]]], window: int = 50) -> float | None:
     if not symbol_rows:
         return None

     above_count = 0
     total_valid = 0

     for symbol, rows in symbol_rows.items():
         if len(rows) < window:
             continue

         close = rows[-1]['close']
         ma = sum([r['close'] for r in rows[-window:]]) / window

         if close > ma:
             above_count += 1
         total_valid += 1

     if total_valid == 0:
         return None

     return (above_count / total_valid) * 100

def calculate_breadth_score(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations:
        return None

    up_ratio = uptrend_ratio(confirmations)
    mom_ratio = momentum_positive_ratio(confirmations)

    if up_ratio is None or mom_ratio is None:
        return None

    # Simple average of up ratio and momentum ratio
    return (up_ratio + mom_ratio) / 2.0

def classify_breadth_regime(confirmations: list[MultiTimeframeRegimeConfirmation]) -> BreadthRegime:
    if len(confirmations) < 20: # Require a minimum universe size
        return BreadthRegime.INSUFFICIENT_DATA

    score = calculate_breadth_score(confirmations)
    if score is None:
        return BreadthRegime.INSUFFICIENT_DATA

    if score > 75:
        return BreadthRegime.BROAD_RISK_ON
    elif score > 60:
        return BreadthRegime.RISK_ON
    elif score < 25:
        return BreadthRegime.RISK_OFF
    elif score < 40:
        return BreadthRegime.DETERIORATING

    return BreadthRegime.MIXED

def breadth_proxy_summary(confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, Any]:
    return {
        "symbol_count": len(confirmations),
        "uptrend_ratio": uptrend_ratio(confirmations),
        "momentum_positive_ratio": momentum_positive_ratio(confirmations),
        "breadth_score": calculate_breadth_score(confirmations),
        "regime": classify_breadth_regime(confirmations).value
    }

def breadth_proxy_summary_to_text(summary: dict[str, Any]) -> str:
    return (
        f"Breadth Regime: {summary['regime']} (Score: {summary['breadth_score']:.1f}) - "
        f"Uptrend Ratio: {summary['uptrend_ratio']:.1f}%, "
        f"Momentum Ratio: {summary['momentum_positive_ratio']:.1f}%"
    )
