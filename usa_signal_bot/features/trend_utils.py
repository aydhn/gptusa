import pandas as pd
import numpy as np
from typing import Dict
from usa_signal_bot.core.exceptions import IndicatorParameterError

def validate_window(value: int, field_name: str, min_value: int = 1, max_value: int = 1000) -> None:
    if not isinstance(value, int):
        raise IndicatorParameterError(f"{field_name} must be an integer, got {type(value)}")
    if value < min_value or value > max_value:
        raise IndicatorParameterError(f"{field_name} must be between {min_value} and {max_value}, got {value}")

def validate_macd_params(fast: int, slow: int, signal: int) -> None:
    validate_window(fast, "fast", min_value=2, max_value=100)
    validate_window(slow, "slow", min_value=3, max_value=200)
    validate_window(signal, "signal", min_value=2, max_value=100)
    if fast >= slow:
        raise IndicatorParameterError(f"MACD fast ({fast}) must be strictly less than slow ({slow})")

def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()

def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def calculate_wma(series: pd.Series, window: int) -> pd.Series:
    weights = np.arange(1, window + 1)
    return series.rolling(window=window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def calculate_dema(series: pd.Series, span: int) -> pd.Series:
    ema1 = calculate_ema(series, span)
    ema2 = calculate_ema(ema1, span)
    return 2 * ema1 - ema2

def calculate_tema(series: pd.Series, span: int) -> pd.Series:
    ema1 = calculate_ema(series, span)
    ema2 = calculate_ema(ema1, span)
    ema3 = calculate_ema(ema2, span)
    return 3 * ema1 - 3 * ema2 + ema3

def calculate_macd(close: pd.Series, fast: int, slow: int, signal: int) -> pd.DataFrame:
    fast_ema = calculate_ema(close, fast)
    slow_ema = calculate_ema(close, slow)
    macd_line = fast_ema - slow_ema
    macd_signal = calculate_ema(macd_line, signal)
    macd_hist = macd_line - macd_signal

    return pd.DataFrame({
        f"macd_{fast}_{slow}_{signal}": macd_line,
        f"macd_signal_{fast}_{slow}_{signal}": macd_signal,
        f"macd_hist_{fast}_{slow}_{signal}": macd_hist
    })

def calculate_series_slope(series: pd.Series, window: int) -> pd.Series:
    # simple slope calculation (price diff over window divided by window)
    return (series - series.shift(window)) / window

def calculate_price_distance_pct(price: pd.Series, reference: pd.Series) -> pd.Series:
    res = (price - reference) / reference
    res = res.replace([np.inf, -np.inf], np.nan)
    return res

def calculate_ma_alignment_score(ma_values: Dict[str, pd.Series]) -> pd.Series:
    if "short" not in ma_values or "medium" not in ma_values or "long" not in ma_values:
        raise ValueError("ma_values dict must contain 'short', 'medium', and 'long' keys")

    short = ma_values["short"]
    medium = ma_values["medium"]
    long = ma_values["long"]

    score = pd.Series(0, index=short.index)

    # Check +1 condition: short > medium > long
    up_trend = (short > medium) & (medium > long)
    score[up_trend] = 1

    # Check -1 condition: short < medium < long
    down_trend = (short < medium) & (medium < long)
    score[down_trend] = -1

    return score
