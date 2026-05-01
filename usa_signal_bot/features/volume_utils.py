import pandas as pd
import numpy as np
from typing import Optional

def validate_volume_window(value: int, field_name: str, min_value: int = 1, max_value: int = 1000) -> None:
    if not isinstance(value, int):
        from usa_signal_bot.core.exceptions import IndicatorParameterError
        raise IndicatorParameterError(f"{field_name} must be an integer")
    if value < min_value or value > max_value:
        from usa_signal_bot.core.exceptions import IndicatorParameterError
        raise IndicatorParameterError(f"{field_name} must be between {min_value} and {max_value}")

def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    price_change = close.diff()
    direction = np.sign(price_change)
    direction = direction.fillna(0)  # first element is 0

    vol_adj = volume * direction
    obv = vol_adj.cumsum()
    return obv

def calculate_vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
    typical_price = (high + low + close) / 3.0
    cum_vol_price = (typical_price * volume).cumsum()
    cum_vol = volume.cumsum()

    vwap = cum_vol_price / cum_vol
    return vwap.replace([np.inf, -np.inf], np.nan)

def calculate_rolling_vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 20) -> pd.Series:
    typical_price = (high + low + close) / 3.0
    vol_price = typical_price * volume

    rolling_vol_price = vol_price.rolling(window=window, min_periods=1).sum()
    rolling_vol = volume.rolling(window=window, min_periods=1).sum()

    vwap = rolling_vol_price / rolling_vol
    return vwap.replace([np.inf, -np.inf], np.nan)

def calculate_money_flow_index(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 14) -> pd.Series:
    typical_price = (high + low + close) / 3.0
    raw_money_flow = typical_price * volume

    direction = np.sign(typical_price.diff())
    direction = direction.fillna(0)

    pos_mf = np.where(direction > 0, raw_money_flow, 0.0)
    neg_mf = np.where(direction < 0, raw_money_flow, 0.0)

    pos_mf_series = pd.Series(pos_mf, index=close.index)
    neg_mf_series = pd.Series(neg_mf, index=close.index)

    pos_mf_sum = pos_mf_series.rolling(window=window, min_periods=1).sum()
    neg_mf_sum = neg_mf_series.rolling(window=window, min_periods=1).sum()

    mfr = pos_mf_sum / neg_mf_sum
    mfi = 100.0 - (100.0 / (1.0 + mfr))
    mfi = mfi.replace([np.inf, -np.inf], 100.0)

    return mfi

def safe_money_flow_multiplier(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    hl_range = high - low
    hl_range = hl_range.replace(0.0, np.nan)
    mfm = ((close - low) - (high - close)) / hl_range
    return mfm.fillna(0.0)

def calculate_chaikin_money_flow(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 20) -> pd.Series:
    mfm = safe_money_flow_multiplier(high, low, close)
    mfv = mfm * volume

    sum_mfv = mfv.rolling(window=window, min_periods=1).sum()
    sum_vol = volume.rolling(window=window, min_periods=1).sum()

    cmf = sum_mfv / sum_vol
    return cmf.replace([np.inf, -np.inf], np.nan)

def calculate_accumulation_distribution_line(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
    mfm = safe_money_flow_multiplier(high, low, close)
    mfv = mfm * volume
    adl = mfv.cumsum()
    return adl

def calculate_volume_sma(volume: pd.Series, window: int = 20) -> pd.Series:
    return volume.rolling(window=window, min_periods=1).mean()

def calculate_volume_ema(volume: pd.Series, span: int = 20) -> pd.Series:
    return volume.ewm(span=span, adjust=False, min_periods=1).mean()

def calculate_relative_volume(volume: pd.Series, window: int = 20) -> pd.Series:
    avg_vol = calculate_volume_sma(volume, window)
    rel_vol = volume / avg_vol
    return rel_vol.replace([np.inf, -np.inf], np.nan)

def calculate_volume_change(volume: pd.Series, periods: int = 1) -> pd.Series:
    return volume.diff(periods=periods)

def calculate_volume_roc(volume: pd.Series, window: int = 10) -> pd.Series:
    shifted_vol = volume.shift(window)
    shifted_vol = shifted_vol.replace(0.0, np.nan) # prevent division by zero
    roc = ((volume - shifted_vol) / shifted_vol) * 100.0
    return roc.replace([np.inf, -np.inf], np.nan)

def calculate_dollar_volume(close: pd.Series, volume: pd.Series) -> pd.Series:
    return close * volume

def calculate_average_dollar_volume(close: pd.Series, volume: pd.Series, window: int = 20) -> pd.Series:
    dv = calculate_dollar_volume(close, volume)
    return dv.rolling(window=window, min_periods=1).mean()

def calculate_volume_trend_strength(volume: pd.Series, close: pd.Series, window: int = 20) -> pd.Series:
    price_change_pct = close.pct_change()
    rel_vol = calculate_relative_volume(volume, window)

    strength = price_change_pct * rel_vol
    return strength.rolling(window=window, min_periods=1).mean().replace([np.inf, -np.inf], np.nan)
