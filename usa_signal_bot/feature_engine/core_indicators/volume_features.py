import pandas as pd
import numpy as np
def add_volume_sma_features(df: pd.DataFrame, windows: list[int] = None) -> pd.DataFrame:
    if not windows: windows = [20]
    for w in windows: df[f'volume_sma_{w}'] = df['volume'].rolling(w).mean()
    df['volume_sma20_ratio'] = df['volume'] / df['volume_sma_20']
    return df
def add_volume_zscore_features(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    vol_mean = df['volume'].rolling(window).mean()
    vol_std = df['volume'].rolling(window).std()
    df[f'volume_zscore_{window}'] = (df['volume'] - vol_mean) / vol_std
    return df
def compute_obv(df: pd.DataFrame) -> pd.Series:
    direction = np.sign(df['close'].diff())
    direction = direction.fillna(0)
    return (direction * df['volume']).cumsum()
def add_obv_feature(df: pd.DataFrame) -> pd.DataFrame:
    df['obv'] = compute_obv(df)
    return df
def add_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_volume_sma_features(df)
    df = add_volume_zscore_features(df)
    df = add_obv_feature(df)
    return df
def validate_volume_features(df: pd.DataFrame) -> list[str]: return []
def volume_features_summary(df: pd.DataFrame) -> dict: return {}
