from typing import Any
from usa_signal_bot.core.enums import TrendRegime
import pandas as pd
import numpy as np

def moving_average(values: list[float], window: int) -> float | None:
    if len(values) < window or window <= 0:
        return None
    return sum(values[-window:]) / window

def slope_proxy(values: list[float], window: int = 20) -> float | None:
    if len(values) < window or window <= 1:
        return None

    y = np.array(values[-window:])
    x = np.arange(len(y))

    # Calculate slope using simple linear regression formula
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean)**2)

    if denominator == 0:
        return 0.0

    slope = numerator / denominator

    # Normalize by price to make it comparable across assets
    normalized_slope = (slope / y_mean) * 100 if y_mean != 0 else 0.0
    return normalized_slope

def price_position_score(rows: list[dict[str, Any]]) -> float | None:
    if not rows:
        return None

    df = pd.DataFrame(rows)
    if len(df) < 50:
        return None

    current_price = df['close'].iloc[-1]
    highest = df['high'].rolling(window=50).max().iloc[-1]
    lowest = df['low'].rolling(window=50).min().iloc[-1]

    if highest == lowest:
        return 50.0

    return ((current_price - lowest) / (highest - lowest)) * 100

def classify_trend_regime(rows: list[dict[str, Any]], short_window: int = 20, long_window: int = 50) -> tuple[TrendRegime, dict[str, Any]]:
    if len(rows) < long_window:
        return TrendRegime.INSUFFICIENT_DATA, {"reason": "Not enough rows"}

    df = pd.DataFrame(rows)
    close_prices = df['close'].tolist()

    short_ma = moving_average(close_prices, short_window)
    long_ma = moving_average(close_prices, long_window)

    if short_ma is None or long_ma is None:
         return TrendRegime.INSUFFICIENT_DATA, {"reason": "Could not compute MAs"}

    current_price = close_prices[-1]

    # Compute slope of short MA
    ma_series = df['close'].rolling(window=short_window).mean().dropna().tolist()
    slope = slope_proxy(ma_series, window=short_window)

    if slope is None:
        slope = 0.0

    ma_distance_pct = abs(short_ma - long_ma) / long_ma * 100 if long_ma != 0 else 0

    evidence = {
        "current_price": current_price,
        "short_ma": short_ma,
        "long_ma": long_ma,
        "slope": slope,
        "ma_distance_pct": ma_distance_pct
    }

    # Heuristics
    if current_price > short_ma and short_ma > long_ma:
        if slope > 0.5 and ma_distance_pct > 2.0:
            return TrendRegime.STRONG_UPTREND, evidence
        return TrendRegime.UPTREND, evidence

    if current_price < short_ma and short_ma < long_ma:
         if slope < -0.5 and ma_distance_pct > 2.0:
             return TrendRegime.STRONG_DOWNTREND, evidence
         return TrendRegime.DOWNTREND, evidence

    if ma_distance_pct < 1.0:
        return TrendRegime.RANGE, evidence

    return TrendRegime.CHOPPY, evidence

def trend_regime_confidence(regime: TrendRegime, evidence: dict[str, Any]) -> float | None:
    if regime == TrendRegime.INSUFFICIENT_DATA:
        return None

    if regime in [TrendRegime.STRONG_UPTREND, TrendRegime.STRONG_DOWNTREND]:
        return 90.0
    elif regime in [TrendRegime.UPTREND, TrendRegime.DOWNTREND]:
        return 70.0
    else:
        return 50.0

def trend_regime_to_text(regime: TrendRegime, evidence: dict[str, Any] | None = None) -> str:
    base_text = f"Trend Regime: {regime.value}"
    if evidence:
        if "slope" in evidence:
            base_text += f", Slope: {evidence['slope']:.2f}"
    return base_text
