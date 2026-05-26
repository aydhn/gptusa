import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any

def compute_pct_return(series: pd.Series, periods: int = 1) -> pd.Series:
    return series.pct_change(periods=periods)

def compute_log_return(series: pd.Series, periods: int = 1) -> pd.Series:
    return np.log(series / series.shift(periods))

def add_daily_return_features(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    df = df.copy()
    if price_col in df.columns:
        df["ret_1d"] = compute_pct_return(df[price_col], 1)
        df["log_ret_1d"] = compute_log_return(df[price_col], 1)
    return df

def add_rolling_return_features(df: pd.DataFrame, windows: Optional[List[int]] = None, price_col: str = "close") -> pd.DataFrame:
    if windows is None: windows = [5, 20]
    df = df.copy()
    if price_col in df.columns:
        for w in windows:
            df[f"ret_{w}d"] = compute_pct_return(df[price_col], w)
    return df

def validate_return_features(df: pd.DataFrame) -> List[str]:
    errors = []
    expected_cols = ["ret_1d", "log_ret_1d", "ret_5d", "ret_20d"]
    for c in expected_cols:
        if c not in df.columns:
            errors.append(f"Missing return feature: {c}")
    return errors
