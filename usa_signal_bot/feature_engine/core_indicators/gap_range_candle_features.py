import pandas as pd
def add_gap_range_candle_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "open" in df.columns and "close" in df.columns:
        prev_close = df["close"].shift(1)
        df["price_gap_pct"] = (df["open"] - prev_close) / prev_close
    return df
