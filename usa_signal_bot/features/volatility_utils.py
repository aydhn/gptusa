import pandas as pd
import numpy as np
from usa_signal_bot.core.exceptions import IndicatorParameterError

def calculate_true_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    hl = high - low
    hc = (high - close.shift(1)).abs()
    lc = (low - close.shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, method: str = "wilder") -> pd.Series:
    tr = calculate_true_range(high, low, close)
    if method == "wilder":
        atr = tr.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    elif method == "sma":
        atr = tr.rolling(window=window, min_periods=window).mean()
    elif method == "ema":
        atr = tr.ewm(span=window, min_periods=window, adjust=False).mean()
    else:
        raise IndicatorParameterError(f"Unsupported ATR method: {method}")
    return atr

def calculate_normalized_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, method: str = "wilder") -> pd.Series:
    atr = calculate_atr(high, low, close, window, method)
    return atr / close

def calculate_bollinger_bands(close: pd.Series, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    middle = close.rolling(window=window, min_periods=window).mean()
    std = close.rolling(window=window, min_periods=window).std()
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)
    return pd.DataFrame({"middle": middle, "upper": upper, "lower": lower})

def calculate_bollinger_bandwidth(upper: pd.Series, middle: pd.Series, lower: pd.Series) -> pd.Series:
    return (upper - lower) / middle

def calculate_bollinger_percent_b(close: pd.Series, upper: pd.Series, lower: pd.Series) -> pd.Series:
    return (close - lower) / (upper - lower)

def calculate_keltner_channels(high: pd.Series, low: pd.Series, close: pd.Series, ema_window: int = 20, atr_window: int = 10, multiplier: float = 2.0) -> pd.DataFrame:
    middle = close.ewm(span=ema_window, min_periods=ema_window, adjust=False).mean()
    atr = calculate_atr(high, low, close, window=atr_window, method="ema")
    upper = middle + (multiplier * atr)
    lower = middle - (multiplier * atr)
    return pd.DataFrame({"middle": middle, "upper": upper, "lower": lower})

def calculate_donchian_channels(high: pd.Series, low: pd.Series, window: int = 20) -> pd.DataFrame:
    upper = high.rolling(window=window, min_periods=window).max()
    lower = low.rolling(window=window, min_periods=window).min()
    middle = (upper + lower) / 2
    return pd.DataFrame({"upper": upper, "middle": middle, "lower": lower})

def calculate_rolling_volatility(close: pd.Series, window: int = 20, annualize: bool = False, periods_per_year: int = 252) -> pd.Series:
    returns = close.pct_change()
    vol = returns.rolling(window=window, min_periods=window).std()
    if annualize:
        vol = vol * np.sqrt(periods_per_year)
    return vol

def calculate_price_range_pct(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    # Divides by close to handle gap cases and keep things percentage based relative to current price level
    return (high - low) / close

def calculate_body_range_pct(open_: pd.Series, close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    # Divides by true range
    tr = calculate_true_range(high, low, close)
    return (close - open_).abs() / tr

def calculate_volatility_compression(current_bandwidth: pd.Series, reference_window: int = 100) -> pd.Series:
    ref_min = current_bandwidth.rolling(window=reference_window, min_periods=reference_window).min()
    return current_bandwidth / ref_min

def calculate_volatility_expansion(current_atr: pd.Series, reference_window: int = 100) -> pd.Series:
    ref_max = current_atr.rolling(window=reference_window, min_periods=reference_window).max()
    return current_atr / ref_max

def validate_volatility_window(value: int, field_name: str, min_value: int = 1, max_value: int = 1000) -> None:
    if not isinstance(value, int):
        raise IndicatorParameterError(f"{field_name} must be an integer")
    if value < min_value or value > max_value:
        raise IndicatorParameterError(f"{field_name} must be between {min_value} and {max_value}")

def validate_band_multiplier(value: float, field_name: str, min_value: float = 0.1, max_value: float = 10.0) -> None:
    if not isinstance(value, (int, float)):
        raise IndicatorParameterError(f"{field_name} must be a number")
    if value < min_value or value > max_value:
        raise IndicatorParameterError(f"{field_name} must be between {min_value} and {max_value}")
