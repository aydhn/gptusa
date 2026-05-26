import pandas as pd
def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    diff = series.diff()
    gain = diff.clip(lower=0).ewm(alpha=1/window, adjust=False).mean()
    loss = (-diff.clip(upper=0)).ewm(alpha=1/window, adjust=False).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
def add_rsi_features(df: pd.DataFrame, price_col: str = "close", windows: list[int] = None) -> pd.DataFrame:
    if not windows: windows = [14]
    for w in windows: df[f'rsi_{w}'] = compute_rsi(df[price_col], w)
    return df
def validate_rsi_features(df: pd.DataFrame) -> list[str]: return []
def rsi_features_summary(df: pd.DataFrame) -> dict: return {}
