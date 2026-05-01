import pandas as pd
import numpy as np
from typing import Optional

def calculate_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/window, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi = rsi.replace([np.inf, -np.inf], 100.0)
    return rsi

def calculate_stochastic_k(high: pd.Series, low: pd.Series, close: pd.Series, k_window: int = 14) -> pd.Series:
    lowest_low = low.rolling(window=k_window).min()
    highest_high = high.rolling(window=k_window).max()
    stoch_k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    return stoch_k.replace([np.inf, -np.inf], np.nan)

def calculate_stochastic_d(stoch_k: pd.Series, d_window: int = 3) -> pd.Series:
    return stoch_k.rolling(window=d_window).mean()

def calculate_roc(close: pd.Series, window: int = 12) -> pd.Series:
    roc = ((close - close.shift(window)) / close.shift(window)) * 100.0
    return roc.replace([np.inf, -np.inf], np.nan)

def calculate_momentum(close: pd.Series, window: int = 10) -> pd.Series:
    return close - close.shift(window)

def calculate_williams_r(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    highest_high = high.rolling(window=window).max()
    lowest_low = low.rolling(window=window).min()
    wr = ((highest_high - close) / (highest_high - lowest_low)) * -100.0
    return wr.replace([np.inf, -np.inf], np.nan)

def calculate_cci(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 20, constant: float = 0.015) -> pd.Series:
    tp = (high + low + close) / 3.0
    sma = tp.rolling(window=window).mean()
    mad = tp.rolling(window=window).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    cci = (tp - sma) / (constant * mad)
    return cci.replace([np.inf, -np.inf], np.nan)

def calculate_momentum_slope(series: pd.Series, slope_window: int = 5) -> pd.Series:
    def _slope(y):
        x = np.arange(len(y))
        if len(y) < slope_window or np.isnan(y).any(): return np.nan
        return np.polyfit(x, y, 1)[0]
    return series.rolling(window=slope_window).apply(_slope, raw=True)

def calculate_momentum_acceleration(series: pd.Series, slope_window: int = 5) -> pd.Series:
    slope = calculate_momentum_slope(series, slope_window)
    return calculate_momentum_slope(slope, slope_window)

def normalize_oscillator_0_100(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val: return pd.Series(50.0, index=series.index)
    return ((series - min_val) / (max_val - min_val)) * 100.0

def clip_series(series: pd.Series, lower: Optional[float] = None, upper: Optional[float] = None) -> pd.Series:
    return series.clip(lower=lower, upper=upper)

def validate_momentum_window(value: int, field_name: str, min_value: int = 1, max_value: int = 500) -> None:
    if not isinstance(value, int): raise TypeError(f"{field_name} must be an integer")
    if value < min_value or value > max_value:
        from usa_signal_bot.core.exceptions import IndicatorParameterError
        raise IndicatorParameterError(f"{field_name} must be between {min_value} and {max_value}")

def validate_stochastic_params(k_window: int, d_window: int) -> None:
    validate_momentum_window(k_window, "k_window", 2, 100)
    validate_momentum_window(d_window, "d_window", 1, 50)
