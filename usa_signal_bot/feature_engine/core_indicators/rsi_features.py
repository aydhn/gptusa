import pandas as pd
def add_rsi_features(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    df = df.copy()
    if price_col in df.columns:
        delta = df[price_col].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=13, adjust=False, min_periods=14).mean()
        ema_down = down.ewm(com=13, adjust=False, min_periods=14).mean()
        rs = ema_up / ema_down
        rsi = 100 - (100 / (1 + rs))
        rsi[ema_down == 0] = 100
        df["rsi_14"] = rsi
    return df
