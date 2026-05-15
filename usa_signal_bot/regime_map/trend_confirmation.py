from typing import Any
import pandas as pd
import numpy as np

from usa_signal_bot.core.enums import TrendRegime
from usa_signal_bot.regime_map.timeframe_resampler import normalize_ohlcv_rows

def classify_trend_regime(rows: list[dict[str, Any]], short_window: int = 20, long_window: int = 50) -> tuple[TrendRegime, dict[str, Any]]:
    rows = normalize_ohlcv_rows(rows)
    evidence = {
        "short_window": short_window,
        "long_window": long_window,
        "close": None,
        "ma_short": None,
        "ma_long": None,
        "slope_short": None,
        "ma_distance_pct": None
    }

    if len(rows) < long_window + 5: # Need some buffer for slope
        return TrendRegime.INSUFFICIENT_DATA, evidence

    closes = [row["close"] for row in rows]
    current_close = closes[-1]
    evidence["close"] = current_close

    ma_short = moving_average(closes, short_window)
    ma_long = moving_average(closes, long_window)
    evidence["ma_short"] = ma_short
    evidence["ma_long"] = ma_long

    if ma_short is None or ma_long is None:
        return TrendRegime.INSUFFICIENT_DATA, evidence

    slope_short = slope_proxy(closes, short_window)
    evidence["slope_short"] = slope_short

    ma_distance_pct = abs(ma_short - ma_long) / ma_long * 100
    evidence["ma_distance_pct"] = ma_distance_pct

    choppy_threshold = 2.0  # Percentage distance to consider choppy if intertwined

    if ma_distance_pct < choppy_threshold and abs(current_close - ma_long)/ma_long*100 < choppy_threshold:
        return TrendRegime.CHOPPY, evidence

    if current_close > ma_short and ma_short > ma_long:
        if slope_short and slope_short > 0:
            if ma_distance_pct > 5.0 and slope_short > 1.0: # Arbitrary thresholds for strong
                return TrendRegime.STRONG_UPTREND, evidence
            return TrendRegime.UPTREND, evidence

    elif current_close < ma_short and ma_short < ma_long:
        if slope_short and slope_short < 0:
            if ma_distance_pct > 5.0 and slope_short < -1.0:
                return TrendRegime.STRONG_DOWNTREND, evidence
            return TrendRegime.DOWNTREND, evidence

    return TrendRegime.RANGE, evidence

def moving_average(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return sum(values[-window:]) / window

def slope_proxy(values: list[float], window: int = 20) -> float | None:
    # Very simple slope proxy: (last - first_of_window) / first_of_window * 100
    if len(values) < window:
        return None
    start_val = values[-window]
    end_val = values[-1]
    if start_val == 0:
        return 0.0
    return (end_val - start_val) / start_val * 100.0

def price_position_score(rows: list[dict[str, Any]]) -> float | None:
    # Where is price relative to recent high/low (e.g., 50 days)
    if len(rows) < 50:
        return None
    recent = rows[-50:]
    highs = [r["high"] for r in recent]
    lows = [r["low"] for r in recent]
    max_h = max(highs)
    min_l = min(lows)
    current = rows[-1]["close"]

    if max_h == min_l:
        return 50.0

    return (current - min_l) / (max_h - min_l) * 100.0

def trend_regime_confidence(regime: TrendRegime, evidence: dict[str, Any]) -> float | None:
    if regime == TrendRegime.INSUFFICIENT_DATA:
        return 0.0

    # Heuristic confidence calculation
    dist = evidence.get("ma_distance_pct", 0)
    slope = abs(evidence.get("slope_short", 0) or 0)

    confidence = min(100.0, 50 + (dist * 2) + (slope * 2))

    if regime in [TrendRegime.CHOPPY, TrendRegime.RANGE]:
        # High confidence in choppy if dist is very low
        confidence = min(100.0, 100.0 - (dist * 10))

    return max(0.0, confidence)

def trend_regime_to_text(regime: TrendRegime, evidence: dict[str, Any] | None = None) -> str:
    text = f"Trend Regime: {regime.value}"
    if evidence:
        text += f" | MA Distance: {evidence.get('ma_distance_pct', 0):.2f}%"
        slope = evidence.get("slope_short")
        if slope is not None:
             text += f" | Slope: {slope:.2f}%"
    return text
