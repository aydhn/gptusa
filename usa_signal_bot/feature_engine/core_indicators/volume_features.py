import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import rolling_mean, rolling_std
def add_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "volume" in df.columns:
        df["volume_sma_20"] = rolling_mean(df["volume"], 20)
    if "close" in df.columns and "volume" in df.columns:
        direction = np.sign(df["close"].diff()).fillna(0)
        df["obv"] = (df["volume"] * direction).cumsum()
    return df
