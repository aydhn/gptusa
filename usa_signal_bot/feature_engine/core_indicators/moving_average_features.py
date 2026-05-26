import pandas as pd
from typing import List, Optional
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import rolling_mean, exponential_moving_average, weighted_moving_average

def add_sma_features(df: pd.DataFrame, windows: Optional[List[int]] = None, price_col: str = "close") -> pd.DataFrame:
    if windows is None: windows = [5, 10, 20, 50]
    df = df.copy()
    if price_col in df.columns:
        for w in windows:
            df[f"sma_{w}"] = rolling_mean(df[price_col], w)
    return df

def add_ema_features(df: pd.DataFrame, spans: Optional[List[int]] = None, price_col: str = "close") -> pd.DataFrame:
    if spans is None: spans = [12, 26]
    df = df.copy()
    if price_col in df.columns:
        for s in spans:
            df[f"ema_{s}"] = exponential_moving_average(df[price_col], s)
    return df

def add_wma_features(df: pd.DataFrame, windows: Optional[List[int]] = None, price_col: str = "close") -> pd.DataFrame:
    if windows is None: windows = [20]
    df = df.copy()
    if price_col in df.columns:
        for w in windows:
            df[f"wma_{w}"] = weighted_moving_average(df[price_col], w)
    return df

def add_moving_average_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_sma_features(df)
    df = add_ema_features(df)
    df = add_wma_features(df)
    return df
