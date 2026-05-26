import pandas as pd
def add_price_action_features(df: pd.DataFrame) -> pd.DataFrame:
    df['close_open_pct'] = (df['close'] - df['open']) / df['open']
    df['close_prev_close_pct'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)
    df['high_close_pct'] = (df['high'] - df['close']) / df['close']
    df['low_close_pct'] = (df['close'] - df['low']) / df['close']
    df['open_prev_close_gap_pct'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)
    return df
def validate_price_action_features(df: pd.DataFrame) -> list[str]: return []
def price_action_features_summary(df: pd.DataFrame) -> dict: return {}
