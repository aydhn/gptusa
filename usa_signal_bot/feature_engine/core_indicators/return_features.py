import pandas as pd
def add_daily_return_features(df: pd.DataFrame) -> pd.DataFrame:
    df['ret_1d'] = df['close'].pct_change(1)
    return df
def compute_pct_return(series: pd.Series, periods: int = 1) -> pd.Series: return series.pct_change(periods)
def compute_log_return(series: pd.Series, periods: int = 1) -> pd.Series:
    import numpy as np
    return np.log(series / series.shift(periods))
def add_rolling_return_features(df: pd.DataFrame, windows: list[int] = None) -> pd.DataFrame:
    if not windows: windows = [5, 20]
    for w in windows: df[f'ret_{w}d'] = df['close'].pct_change(w)
    df['log_ret_1d'] = compute_log_return(df['close'], 1)
    return df
def validate_return_features(df: pd.DataFrame) -> list[str]: return []
def return_features_summary(df: pd.DataFrame) -> dict: return {}
