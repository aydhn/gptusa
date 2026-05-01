import pandas as pd
import numpy as np
from usa_signal_bot.core.exceptions import IndicatorParameterError

def validate_price_action_window(value: int, field_name: str, min_value: int = 1, max_value: int = 1000) -> None:
    if not isinstance(value, int):
        raise IndicatorParameterError(f"{field_name} must be an integer")
    if value < min_value or value > max_value:
        raise IndicatorParameterError(f"{field_name} must be between {min_value} and {max_value}")

def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator.divide(denominator).replace([np.inf, -np.inf], np.nan)

def calculate_candle_body(open_: pd.Series, close: pd.Series) -> pd.Series:
    return (close - open_).abs()

def calculate_candle_body_pct(open_: pd.Series, close: pd.Series) -> pd.Series:
    return safe_divide(calculate_candle_body(open_, close), open_)

def calculate_upper_wick(open_: pd.Series, high: pd.Series, close: pd.Series) -> pd.Series:
    max_oc = pd.concat([open_, close], axis=1).max(axis=1)
    return (high - max_oc).clip(lower=0)

def calculate_lower_wick(open_: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    min_oc = pd.concat([open_, close], axis=1).min(axis=1)
    return (min_oc - low).clip(lower=0)

def calculate_upper_wick_pct(open_: pd.Series, high: pd.Series, close: pd.Series) -> pd.Series:
    return safe_divide(calculate_upper_wick(open_, high, close), open_)

def calculate_lower_wick_pct(open_: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    return safe_divide(calculate_lower_wick(open_, low, close), open_)

def calculate_full_range(high: pd.Series, low: pd.Series) -> pd.Series:
    return (high - low).clip(lower=0)

def calculate_full_range_pct(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    return safe_divide(calculate_full_range(high, low), close.shift(1))

def calculate_close_location_value(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    clv = safe_divide((close - low), (high - low))
    return clv.clip(lower=0, upper=1)

def calculate_gap_pct(open_: pd.Series, previous_close: pd.Series) -> pd.Series:
    return safe_divide(open_ - previous_close, previous_close)

def calculate_breakout_distance_pct(close: pd.Series, high: pd.Series, window: int = 20) -> pd.Series:
    validate_price_action_window(window, "window", min_value=2)
    rolling_high_prev = high.shift(1).rolling(window=window).max()
    return safe_divide(close - rolling_high_prev, rolling_high_prev)

def calculate_breakdown_distance_pct(close: pd.Series, low: pd.Series, window: int = 20) -> pd.Series:
    validate_price_action_window(window, "window", min_value=2)
    rolling_low_prev = low.shift(1).rolling(window=window).min()
    return safe_divide(close - rolling_low_prev, rolling_low_prev)

def detect_inside_bar(high: pd.Series, low: pd.Series) -> pd.Series:
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    is_inside = (high <= prev_high) & (low >= prev_low)
    return is_inside.astype(int)

def detect_outside_bar(high: pd.Series, low: pd.Series) -> pd.Series:
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    is_outside = (high > prev_high) & (low < prev_low)
    return is_outside.astype(int)

def detect_swing_high(high: pd.Series, left_window: int = 2, right_window: int = 2) -> pd.Series:
    validate_price_action_window(left_window, "left_window", min_value=1)
    validate_price_action_window(right_window, "right_window", min_value=1)

    window = left_window + right_window + 1
    rolling_max = high.rolling(window=window, center=True).max()
    is_swing_high = (high == rolling_max)

    return is_swing_high.shift(right_window).fillna(0).astype(int)

def detect_swing_low(low: pd.Series, left_window: int = 2, right_window: int = 2) -> pd.Series:
    validate_price_action_window(left_window, "left_window", min_value=1)
    validate_price_action_window(right_window, "right_window", min_value=1)

    window = left_window + right_window + 1
    rolling_min = low.rolling(window=window, center=True).min()
    is_swing_low = (low == rolling_min)

    return is_swing_low.shift(right_window).fillna(0).astype(int)

def calculate_higher_high(high: pd.Series, swing_high: pd.Series) -> pd.Series:
    swing_high_values = high.where(swing_high == 1)
    prev_swing_high_values = swing_high_values.ffill().shift(1)

    is_higher_high = (swing_high == 1) & (high > prev_swing_high_values)
    return is_higher_high.fillna(0).astype(int)

def calculate_lower_low(low: pd.Series, swing_low: pd.Series) -> pd.Series:
    swing_low_values = low.where(swing_low == 1)
    prev_swing_low_values = swing_low_values.ffill().shift(1)

    is_lower_low = (swing_low == 1) & (low < prev_swing_low_values)
    return is_lower_low.fillna(0).astype(int)

def calculate_range_expansion(high: pd.Series, low: pd.Series, window: int = 20) -> pd.Series:
    validate_price_action_window(window, "window", min_value=2)
    current_range = calculate_full_range(high, low)
    avg_range_prev = current_range.shift(1).rolling(window=window).mean()
    return safe_divide(current_range, avg_range_prev)

def calculate_range_contraction(high: pd.Series, low: pd.Series, window: int = 20) -> pd.Series:
    validate_price_action_window(window, "window", min_value=2)
    current_range = calculate_full_range(high, low)
    avg_range_prev = current_range.shift(1).rolling(window=window).mean()
    return safe_divide(avg_range_prev, current_range)
