import pandas as pd
def compute_bollinger_bands(series: pd.Series, window: int = 20, num_std: float = 2.0):
    mid = series.rolling(window).mean()
    std = series.rolling(window).std()
    return mid, mid + num_std * std, mid - num_std * std
def add_bollinger_features(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    mid, up, low = compute_bollinger_bands(df[price_col])
    df['bb_mid_20'] = mid
    df['bb_upper_20_2'] = up
    df['bb_lower_20_2'] = low
    df['bb_width_20_2'] = (up - low) / mid
    df['bb_percent_b_20_2'] = (df[price_col] - low) / (up - low)
    return df
def validate_bollinger_features(df: pd.DataFrame) -> list[str]: return []
def bollinger_features_summary(df: pd.DataFrame) -> dict: return {}
