import pandas as pd
from typing import Optional, List

def validate_rolling_window(window: int, min_periods: Optional[int] = None) -> List[str]:
    errors = []
    if window <= 0: errors.append("window must be > 0")
    if min_periods is not None:
        if min_periods <= 0: errors.append("min_periods must be > 0")
        if min_periods > window: errors.append("min_periods cannot exceed window")
    return errors

def rolling_mean(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_p = min_periods if min_periods is not None else window
    return series.rolling(window=window, min_periods=min_p).mean()

def rolling_std(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_p = min_periods if min_periods is not None else window
    return series.rolling(window=window, min_periods=min_p).std()

def rolling_min(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_p = min_periods if min_periods is not None else window
    return series.rolling(window=window, min_periods=min_p).min()

def rolling_max(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_p = min_periods if min_periods is not None else window
    return series.rolling(window=window, min_periods=min_p).max()

def rolling_sum(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_p = min_periods if min_periods is not None else window
    return series.rolling(window=window, min_periods=min_p).sum()

def exponential_moving_average(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False, min_periods=span).mean()

def weighted_moving_average(series: pd.Series, window: int) -> pd.Series:
    def wma(s):
        weights = list(range(1, len(s) + 1))
        return (s * weights).sum() / sum(weights)
    return series.rolling(window=window, min_periods=window).apply(wma, raw=True)
