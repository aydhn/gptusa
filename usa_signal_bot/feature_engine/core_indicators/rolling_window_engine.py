import pandas as pd
def rolling_mean(series: pd.Series, window: int, min_periods: int = None) -> pd.Series: return series.rolling(window, min_periods=min_periods).mean()
def rolling_std(series: pd.Series, window: int, min_periods: int = None) -> pd.Series: return series.rolling(window, min_periods=min_periods).std()
def rolling_min(series: pd.Series, window: int, min_periods: int = None) -> pd.Series: return series.rolling(window, min_periods=min_periods).min()
def rolling_max(series: pd.Series, window: int, min_periods: int = None) -> pd.Series: return series.rolling(window, min_periods=min_periods).max()
def rolling_sum(series: pd.Series, window: int, min_periods: int = None) -> pd.Series: return series.rolling(window, min_periods=min_periods).sum()
def exponential_moving_average(series: pd.Series, span: int) -> pd.Series: return series.ewm(span=span, adjust=False).mean()
def weighted_moving_average(series: pd.Series, window: int) -> pd.Series:
    import numpy as np
    weights = np.arange(1, window + 1)
    return series.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
def validate_rolling_window(window: int, min_periods: int = None) -> list[str]:
    if window <= 0: return ["window must be > 0"]
    return []
def rolling_window_summary(df: pd.DataFrame, columns: list[str]) -> dict: return {}
