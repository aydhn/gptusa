import pandas as pd
import numpy as np
def add_gap_features(df: pd.DataFrame) -> pd.DataFrame:
    df['price_gap_pct'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)
    return df
def add_range_features(df: pd.DataFrame) -> pd.DataFrame:
    df['intraday_range_pct'] = (df['high'] - df['low']) / df['low']
    return df
def add_candle_shape_features(df: pd.DataFrame) -> pd.DataFrame:
    df['candle_body_pct'] = (df['close'] - df['open']).abs() / df['open']
    top_body = df[['open', 'close']].max(axis=1)
    bottom_body = df[['open', 'close']].min(axis=1)
    df['upper_shadow_pct'] = (df['high'] - top_body) / top_body
    df['lower_shadow_pct'] = (bottom_body - df['low']) / bottom_body
    return df
def add_gap_range_candle_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_gap_features(df)
    df = add_range_features(df)
    df = add_candle_shape_features(df)
    return df
def validate_gap_range_candle_features(df: pd.DataFrame) -> list[str]: return []
def gap_range_candle_features_summary(df: pd.DataFrame) -> dict: return {}
