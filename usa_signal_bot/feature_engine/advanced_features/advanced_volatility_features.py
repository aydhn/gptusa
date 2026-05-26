import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.exceptions import AdvancedVolatilityFeatureError

def add_realized_volatility_features(df: pd.DataFrame, windows: Optional[List[int]] = None, return_col: str = "ret_1d") -> pd.DataFrame:
    """Computes realized volatility over given windows."""
    if windows is None:
        windows = [10, 20]
    df_out = df.copy()
    if return_col not in df_out.columns:
        raise AdvancedVolatilityFeatureError(f"Missing return column: {return_col}")

    for w in windows:
        # Assuming ret_1d is daily return, annualized volatility = std * sqrt(252)
        # However, for pure feature generation we will just output rolling std.
        col_name = f"realized_vol_{w}"
        df_out[col_name] = df_out[return_col].rolling(window=w, min_periods=w//2).std()

    return df_out

def add_downside_upside_volatility_features(df: pd.DataFrame, window: int = 20, return_col: str = "ret_1d") -> pd.DataFrame:
    """Computes downside and upside volatility."""
    df_out = df.copy()
    if return_col not in df_out.columns:
        raise AdvancedVolatilityFeatureError(f"Missing return column: {return_col}")

    downside_returns = df_out[return_col].copy()
    downside_returns[downside_returns > 0] = 0
    upside_returns = df_out[return_col].copy()
    upside_returns[upside_returns < 0] = 0

    df_out[f"downside_vol_{window}"] = downside_returns.rolling(window=window, min_periods=window//2).std()
    df_out[f"upside_vol_{window}"] = upside_returns.rolling(window=window, min_periods=window//2).std()

    return df_out

def add_volatility_of_volatility_features(df: pd.DataFrame, window: int = 20, vol_col: str = "rolling_vol_20") -> pd.DataFrame:
    """Computes volatility of volatility."""
    df_out = df.copy()

    # If standard rolling_vol_20 doesn't exist, compute it on the fly from ret_1d
    if vol_col not in df_out.columns:
        if "ret_1d" in df_out.columns:
            df_out[vol_col] = df_out["ret_1d"].rolling(window=window, min_periods=window//2).std()
        else:
            raise AdvancedVolatilityFeatureError(f"Missing volatility column: {vol_col} and 'ret_1d'")

    df_out[f"vol_of_vol_{window}"] = df_out[vol_col].rolling(window=window, min_periods=window//2).std()

    return df_out

def add_atr_percentile_features(df: pd.DataFrame, window: int = 60, atr_col: str = "atr_14") -> pd.DataFrame:
    """Computes ATR percentile features."""
    df_out = df.copy()

    if atr_col not in df_out.columns:
        # Fallback to computing True Range -> ATR
        if all(c in df_out.columns for c in ["high", "low", "close"]):
            high_low = df_out["high"] - df_out["low"]
            high_close = (df_out["high"] - df_out["close"].shift(1)).abs()
            low_close = (df_out["low"] - df_out["close"].shift(1)).abs()
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            df_out[atr_col] = tr.rolling(window=14, min_periods=7).mean()
        else:
            raise AdvancedVolatilityFeatureError(f"Missing ATR column: {atr_col}")

    def percentile_rank(s: pd.Series) -> float:
        if len(s.dropna()) == 0:
            return np.nan
        return pd.Series(s).rank(pct=True).iloc[-1]

    df_out[f"atr_percentile_{window}"] = df_out[atr_col].rolling(window=window, min_periods=window//2).apply(percentile_rank, raw=False)

    # Also atr zscore
    mean = df_out[atr_col].rolling(window=window, min_periods=window//2).mean()
    std = df_out[atr_col].rolling(window=window, min_periods=window//2).std()
    df_out[f"atr_zscore_{window}"] = (df_out[atr_col] - mean) / std

    return df_out

def add_advanced_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs all advanced volatility feature generators."""
    df_out = df.copy()

    # Calculate daily returns if not present
    if "ret_1d" not in df_out.columns and "close" in df_out.columns:
        df_out["ret_1d"] = df_out["close"].pct_change()

    df_out = add_realized_volatility_features(df_out)
    df_out = add_downside_upside_volatility_features(df_out)
    df_out = add_volatility_of_volatility_features(df_out)
    df_out = add_atr_percentile_features(df_out)

    return df_out

def validate_advanced_volatility_features(df: pd.DataFrame) -> List[str]:
    errors = []
    required = [
        "realized_vol_10", "realized_vol_20",
        "downside_vol_20", "upside_vol_20",
        "vol_of_vol_20", "atr_percentile_60", "atr_zscore_60"
    ]
    for col in required:
        if col not in df.columns:
            errors.append(f"Missing required volatility column: {col}")
    return errors

def advanced_volatility_features_summary(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "columns_present": [c for c in df.columns if c in [
            "realized_vol_10", "realized_vol_20",
            "downside_vol_20", "upside_vol_20",
            "vol_of_vol_20", "atr_percentile_60", "atr_zscore_60"
        ]],
        "is_valid": len(validate_advanced_volatility_features(df)) == 0
    }
