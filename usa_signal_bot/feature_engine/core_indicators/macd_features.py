import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import exponential_moving_average
def add_macd_features(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    df = df.copy()
    if price_col in df.columns:
        ema_fast = exponential_moving_average(df[price_col], 12)
        ema_slow = exponential_moving_average(df[price_col], 26)
        macd = ema_fast - ema_slow
        macd_signal = exponential_moving_average(macd, 9)
        df["macd_12_26"] = macd
        df["macd_signal_9"] = macd_signal
        df["macd_hist"] = macd - macd_signal
    return df
