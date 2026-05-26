import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.exceptions import AdvancedTrendFeatureError

def rolling_linear_slope(series: pd.Series, window: int) -> pd.Series:
    """Computes the linear regression slope over a rolling window."""
    def slope(y):
        if len(y) < 2 or np.isnan(y).any():
            return np.nan
        x = np.arange(len(y))
        # Simple linear regression slope formula
        n = len(y)
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_x2 = np.sum(x**2)
        sum_xy = np.sum(x * y)
        denom = (n * sum_x2 - sum_x**2)
        if denom == 0:
            return np.nan
        return (n * sum_xy - sum_x * sum_y) / denom

    return series.rolling(window=window, min_periods=window//2).apply(slope, raw=True)

def add_trend_slope_features(df: pd.DataFrame, windows: Optional[List[int]] = None, price_col: str = "close") -> pd.DataFrame:
    """Adds linear trend slope features for multiple horizons."""
    if windows is None:
        windows = [20, 60]
    df_out = df.copy()
    if price_col not in df_out.columns:
        raise AdvancedTrendFeatureError(f"Missing price column: {price_col}")

    for w in windows:
        df_out[f"trend_slope_{w}"] = rolling_linear_slope(df_out[price_col], w)

    return df_out

def add_trend_strength_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes an ad-hoc trend strength proxy using R-squared of the linear fit."""
    # For performance, we'll proxy trend strength as absolute slope / volatility
    df_out = df.copy()

    if "close" not in df_out.columns:
        raise AdvancedTrendFeatureError("Missing 'close' column")

    if "trend_slope_20" not in df_out.columns:
        df_out = add_trend_slope_features(df_out, windows=[20, 60])

    # Proxy: normalized slope
    close_std_20 = df_out["close"].rolling(20, min_periods=10).std()
    close_std_60 = df_out["close"].rolling(60, min_periods=30).std()

    df_out["trend_strength_20"] = (df_out["trend_slope_20"].abs() / close_std_20).replace([np.inf, -np.inf], np.nan)
    df_out["trend_strength_60"] = (df_out["trend_slope_60"].abs() / close_std_60).replace([np.inf, -np.inf], np.nan)

    return df_out

def add_ma_distance_normalized_features(df: pd.DataFrame, window: int = 60) -> pd.DataFrame:
    """Computes the z-score of the distance between close and moving averages."""
    df_out = df.copy()
    if "close" not in df_out.columns:
        raise AdvancedTrendFeatureError("Missing 'close' column")

    sma_20 = df_out["close"].rolling(20, min_periods=10).mean()
    sma_50 = df_out["close"].rolling(50, min_periods=25).mean()

    dist_20 = df_out["close"] - sma_20
    dist_50 = df_out["close"] - sma_50

    mean_20 = dist_20.rolling(window=window, min_periods=window//2).mean()
    std_20 = dist_20.rolling(window=window, min_periods=window//2).std()
    df_out[f"close_to_sma20_zscore_{window}"] = (dist_20 - mean_20) / std_20

    mean_50 = dist_50.rolling(window=window, min_periods=window//2).mean()
    std_50 = dist_50.rolling(window=window, min_periods=window//2).std()
    df_out[f"close_to_sma50_zscore_{window}"] = (dist_50 - mean_50) / std_50

    return df_out

def add_advanced_trend_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs all advanced trend feature generators."""
    df_out = add_trend_slope_features(df)
    df_out = add_trend_strength_features(df_out)
    df_out = add_ma_distance_normalized_features(df_out)
    return df_out

def validate_advanced_trend_features(df: pd.DataFrame) -> List[str]:
    errors = []
    required = [
        "trend_slope_20", "trend_slope_60",
        "trend_strength_20", "trend_strength_60",
        "close_to_sma20_zscore_60", "close_to_sma50_zscore_60"
    ]
    for col in required:
        if col not in df.columns:
            errors.append(f"Missing required trend column: {col}")
    return errors

def advanced_trend_features_summary(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "columns_present": [c for c in df.columns if c in [
            "trend_slope_20", "trend_slope_60",
            "trend_strength_20", "trend_strength_60",
            "close_to_sma20_zscore_60", "close_to_sma50_zscore_60"
        ]],
        "is_valid": len(validate_advanced_trend_features(df)) == 0
    }
