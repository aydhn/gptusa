import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import rolling_mean

def compute_true_range(df: pd.DataFrame) -> pd.Series:
    if not all(c in df.columns for c in ["high", "low", "close"]):
        return pd.Series(np.nan, index=df.index)
    prev_close = df["close"].shift(1)
    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - prev_close).abs()
    tr3 = (df["low"] - prev_close).abs()
    return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

def add_true_range_atr_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    tr = compute_true_range(df)
    df["true_range"] = tr
    df["atr_14"] = rolling_mean(tr, 14)
    return df
