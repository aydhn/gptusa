import pandas as pd
def add_rolling_volatility_features(df: pd.DataFrame, windows: list[int] = None, return_col: str = "ret_1d") -> pd.DataFrame:
    if return_col not in df.columns: df[return_col] = df['close'].pct_change(1)
    if not windows: windows = [5, 20]
    for w in windows: df[f'rolling_vol_{w}'] = df[return_col].rolling(w).std()
    return df
def add_price_range_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    df['high_low_range_pct'] = (df['high'] - df['low']) / df['low']
    df['close_to_high_pct'] = (df['high'] - df['close']) / df['close']
    df['close_to_low_pct'] = (df['close'] - df['low']) / df['close']
    return df
def compute_rolling_volatility(series: pd.Series, window: int) -> pd.Series: return series.rolling(window).std()
def validate_volatility_features(df: pd.DataFrame) -> list[str]: return []
def volatility_features_summary(df: pd.DataFrame) -> dict: return {}
