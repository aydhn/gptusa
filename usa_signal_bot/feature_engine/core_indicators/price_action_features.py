import pandas as pd
def add_price_action_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if all(c in df.columns for c in ["open", "close"]):
        df["close_open_pct"] = (df["close"] - df["open"]) / df["open"]
    return df
