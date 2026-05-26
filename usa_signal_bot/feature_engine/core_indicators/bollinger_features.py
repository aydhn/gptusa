import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import rolling_mean, rolling_std
def add_bollinger_features(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    df = df.copy()
    if price_col in df.columns:
        mid = rolling_mean(df[price_col], 20)
        std = rolling_std(df[price_col], 20)
        df["bb_mid_20"] = mid
        df["bb_upper_20_2"] = mid + (std * 2.0)
        df["bb_lower_20_2"] = mid - (std * 2.0)
    return df
