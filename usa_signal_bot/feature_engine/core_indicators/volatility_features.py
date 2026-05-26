import pandas as pd
from typing import List, Optional
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import rolling_std

def add_rolling_volatility_features(df: pd.DataFrame, windows: Optional[List[int]] = None, return_col: str = "ret_1d") -> pd.DataFrame:
    if windows is None: windows = [5, 20]
    df = df.copy()
    if return_col in df.columns:
        for w in windows:
            df[f"rolling_vol_{w}"] = rolling_std(df[return_col], w)
    return df

def add_price_range_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if all(c in df.columns for c in ["high", "low", "close"]):
        df["high_low_range_pct"] = (df["high"] - df["low"]) / df["close"]
        df["close_to_high_pct"] = (df["high"] - df["close"]) / df["close"]
        df["close_to_low_pct"] = (df["close"] - df["low"]) / df["close"]
    return df
