import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import rolling_min, rolling_max, rolling_mean
def add_stochastic_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if all(c in df.columns for c in ["high", "low", "close"]):
        roll_low = rolling_min(df["low"], 14)
        roll_high = rolling_max(df["high"], 14)
        k = 100 * ((df["close"] - roll_low) / (roll_high - roll_low))
        df["stoch_k_14"] = k
        df["stoch_d_3"] = rolling_mean(k, 3)
    return df
