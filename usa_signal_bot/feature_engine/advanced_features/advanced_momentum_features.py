import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.exceptions import AdvancedMomentumFeatureError

def add_multi_horizon_momentum_features(df: pd.DataFrame, windows: Optional[List[int]] = None, price_col: str = "close") -> pd.DataFrame:
    """Computes rate of change momentum over multiple horizons."""
    if windows is None:
        windows = [20, 60, 120]
    df_out = df.copy()
    if price_col not in df_out.columns:
        raise AdvancedMomentumFeatureError(f"Missing price column: {price_col}")

    for w in windows:
        col_name = f"momentum_{w}"
        df_out[col_name] = df_out[price_col].pct_change(periods=w)

    return df_out

def add_momentum_acceleration_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes momentum acceleration (diff between short and long momentum)."""
    df_out = df.copy()

    # Ensure mom_20 and mom_60 exist
    if "momentum_20" not in df_out.columns or "momentum_60" not in df_out.columns:
        df_out = add_multi_horizon_momentum_features(df_out, [20, 60])

    df_out["momentum_accel_20_60"] = df_out["momentum_20"] - df_out["momentum_60"]
    return df_out

def add_rsi_normalized_features(df: pd.DataFrame, window: int = 60) -> pd.DataFrame:
    """Computes z-score of RSI over a rolling window."""
    df_out = df.copy()

    rsi_col = "rsi_14"
    if rsi_col not in df_out.columns:
        # compute dummy RSI if not found
        if "close" in df_out.columns:
            delta = df_out["close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=7).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=7).mean()
            rs = gain / loss
            df_out[rsi_col] = 100 - (100 / (1 + rs))
        else:
            raise AdvancedMomentumFeatureError("Missing rsi_14 and close columns")

    mean = df_out[rsi_col].rolling(window=window, min_periods=window//2).mean()
    std = df_out[rsi_col].rolling(window=window, min_periods=window//2).std()
    df_out[f"rsi_14_zscore_{window}"] = (df_out[rsi_col] - mean) / std

    return df_out

def add_macd_hist_normalized_features(df: pd.DataFrame, window: int = 60) -> pd.DataFrame:
    """Computes z-score of MACD histogram over a rolling window."""
    df_out = df.copy()

    macd_hist_col = "macd_hist"
    if macd_hist_col not in df_out.columns:
        # compute basic MACD if missing
        if "close" in df_out.columns:
            ema12 = df_out["close"].ewm(span=12, adjust=False).mean()
            ema26 = df_out["close"].ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9, adjust=False).mean()
            df_out[macd_hist_col] = macd - signal
        else:
            raise AdvancedMomentumFeatureError("Missing macd_hist and close columns")

    mean = df_out[macd_hist_col].rolling(window=window, min_periods=window//2).mean()
    std = df_out[macd_hist_col].rolling(window=window, min_periods=window//2).std()
    df_out[f"macd_hist_zscore_{window}"] = (df_out[macd_hist_col] - mean) / std

    return df_out

def add_advanced_momentum_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs all advanced momentum feature generators."""
    df_out = add_multi_horizon_momentum_features(df)
    df_out = add_momentum_acceleration_features(df_out)
    df_out = add_rsi_normalized_features(df_out)
    df_out = add_macd_hist_normalized_features(df_out)
    return df_out

def validate_advanced_momentum_features(df: pd.DataFrame) -> List[str]:
    errors = []
    required = [
        "momentum_20", "momentum_60", "momentum_120",
        "momentum_accel_20_60", "rsi_14_zscore_60", "macd_hist_zscore_60"
    ]
    for col in required:
        if col not in df.columns:
            errors.append(f"Missing required momentum column: {col}")
    return errors

def advanced_momentum_features_summary(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "columns_present": [c for c in df.columns if c in [
            "momentum_20", "momentum_60", "momentum_120",
            "momentum_accel_20_60", "rsi_14_zscore_60", "macd_hist_zscore_60"
        ]],
        "is_valid": len(validate_advanced_momentum_features(df)) == 0
    }
