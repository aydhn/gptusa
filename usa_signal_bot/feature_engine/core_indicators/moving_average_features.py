import pandas as pd
def add_sma_features(df: pd.DataFrame, windows: list[int] = None, price_col: str = "close") -> pd.DataFrame:
    if not windows: windows = [5, 10, 20, 50]
    for w in windows: df[f'sma_{w}'] = df[price_col].rolling(w).mean()
    return df
def add_ema_features(df: pd.DataFrame, spans: list[int] = None, price_col: str = "close") -> pd.DataFrame:
    if not spans: spans = [12, 26]
    for s in spans: df[f'ema_{s}'] = df[price_col].ewm(span=s, adjust=False).mean()
    return df
def add_wma_features(df: pd.DataFrame, windows: list[int] = None, price_col: str = "close") -> pd.DataFrame:
    if not windows: windows = [20]
    import numpy as np
    for w in windows:
        weights = np.arange(1, w + 1)
        df[f'wma_{w}'] = df[price_col].rolling(w).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    return df
def add_moving_average_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_sma_features(df)
    df = add_ema_features(df)
    df = add_wma_features(df)
    df['close_sma20_ratio'] = df['close'] / df['sma_20']
    df['ema12_ema26_diff'] = df['ema_12'] - df['ema_26']
    return df
def validate_moving_average_features(df: pd.DataFrame) -> list[str]: return []
def moving_average_features_summary(df: pd.DataFrame) -> dict: return {}
