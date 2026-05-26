import pandas as pd
import numpy as np
def compute_true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df['close'].shift(1)
    tr1 = df['high'] - df['low']
    tr2 = (df['high'] - prev_close).abs()
    tr3 = (df['low'] - prev_close).abs()
    return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
def compute_atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    tr = compute_true_range(df)
    return tr.rolling(window).mean()
def add_true_range_atr_features(df: pd.DataFrame) -> pd.DataFrame:
    df['true_range'] = compute_true_range(df)
    df['atr_14'] = compute_atr(df, 14)
    df['atr14_close_ratio'] = df['atr_14'] / df['close']
    return df
def validate_true_range_atr_features(df: pd.DataFrame) -> list[str]: return []
def true_range_atr_features_summary(df: pd.DataFrame) -> dict: return {}
