import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from usa_signal_bot.core.exceptions import NormalizationFeatureError
from usa_signal_bot.core.enums import NormalizationMethod
from usa_signal_bot.feature_engine.advanced_features.phase118_models import NormalizationResult, create_normalization_result_id

def _now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def rolling_zscore(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_periods = min_periods or window // 2
    mean = series.rolling(window=window, min_periods=min_periods).mean()
    std = series.rolling(window=window, min_periods=min_periods).std()
    return (series - mean) / std

def rolling_robust_zscore(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_periods = min_periods or window // 2
    median = series.rolling(window=window, min_periods=min_periods).median()
    # MAD (Median Absolute Deviation)
    mad = series.rolling(window=window, min_periods=min_periods).apply(lambda x: np.median(np.abs(x - np.median(x))), raw=True)
    # scale factor for normal distribution
    mad_scaled = mad * 1.4826
    # Avoid division by zero
    mad_scaled = mad_scaled.replace(0, np.nan)
    return (series - median) / mad_scaled

def rolling_minmax(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_periods = min_periods or window // 2
    vmin = series.rolling(window=window, min_periods=min_periods).min()
    vmax = series.rolling(window=window, min_periods=min_periods).max()
    denom = (vmax - vmin).replace(0, np.nan)
    return (series - vmin) / denom

def rolling_percentile_rank(series: pd.Series, window: int, min_periods: Optional[int] = None) -> pd.Series:
    min_periods = min_periods or window // 2
    def pct_rank(s):
        s_clean = s[~np.isnan(s)]
        if len(s_clean) < min_periods:
            return np.nan
        return pd.Series(s_clean).rank(pct=True).iloc[-1]
    return series.rolling(window=window, min_periods=min_periods).apply(pct_rank, raw=True)

def winsorize_series(series: pd.Series, lower_pct: float = 0.01, upper_pct: float = 0.99) -> pd.Series:
    lower_bound = series.quantile(lower_pct)
    upper_bound = series.quantile(upper_pct)
    return series.clip(lower=lower_bound, upper=upper_bound)

def add_normalization_features(df: pd.DataFrame, columns: List[str], window: int = 60) -> Tuple[pd.DataFrame, List[NormalizationResult]]:
    """Applies multiple normalizations (zscore, percentile) to specified columns."""
    df_out = df.copy()
    results = []

    for col in columns:
        if col not in df_out.columns:
            continue

        # Z-Score
        z_col = f"{col}_zscore_{window}"
        df_out[z_col] = rolling_zscore(df_out[col], window)
        results.append(NormalizationResult(
            normalization_id=create_normalization_result_id(),
            created_at_utc=_now(),
            method=NormalizationMethod.Z_SCORE,
            input_column=col,
            output_column=z_col,
            row_count=len(df_out),
            null_count=int(df_out[z_col].isna().sum()),
            finite_value_count=int(np.isfinite(df_out[z_col]).sum()),
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

        # Percentile Rank
        pct_col = f"{col}_percentile_{window}"
        df_out[pct_col] = rolling_percentile_rank(df_out[col], window)
        results.append(NormalizationResult(
            normalization_id=create_normalization_result_id(),
            created_at_utc=_now(),
            method=NormalizationMethod.PERCENTILE_RANK,
            input_column=col,
            output_column=pct_col,
            row_count=len(df_out),
            null_count=int(df_out[pct_col].isna().sum()),
            finite_value_count=int(np.isfinite(df_out[pct_col]).sum()),
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    return df_out, results

def validate_normalization_features(df: pd.DataFrame) -> List[str]:
    # It's flexible, so no strict hardcoded required columns by default
    # But this can verify schema if needed
    return []

def normalization_features_summary(results: List[NormalizationResult]) -> Dict[str, Any]:
    return {
        "total_normalizations": len(results),
        "methods_used": list(set(r.method.value for r in results)),
        "columns_processed": list(set(r.input_column for r in results))
    }
