from typing import Any
import pandas as pd
from datetime import datetime

from usa_signal_bot.core.enums import RegimeTimeframe
from usa_signal_bot.core.exceptions import TimeframeResamplerError

def normalize_ohlcv_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []
    required_keys = {"date", "open", "high", "low", "close", "volume"}
    for row in rows:
        if not required_keys.issubset(row.keys()):
            raise TimeframeResamplerError(f"Missing required keys in OHLCV row. Required: {required_keys}")

    # Sort by date
    try:
        sorted_rows = sorted(rows, key=lambda x: pd.to_datetime(x["date"]))
    except Exception as e:
        raise TimeframeResamplerError(f"Failed to sort rows by date: {e}")
    return sorted_rows

def rows_to_dataframe_safe(rows: list[dict[str, Any]]) -> pd.DataFrame:
    try:
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        return df
    except Exception as e:
        raise TimeframeResamplerError(f"Failed to convert rows to DataFrame: {e}")

def dataframe_to_ohlcv_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    df = df.reset_index()
    df["date"] = df["date"].dt.strftime('%Y-%m-%d')
    return df.to_dict(orient="records")

def resample_ohlcv_rows(rows: list[dict[str, Any]], timeframe: RegimeTimeframe) -> list[dict[str, Any]]:
    if not rows:
        return []

    if timeframe == RegimeTimeframe.DAILY:
        return normalize_ohlcv_rows(rows)
    elif timeframe == RegimeTimeframe.WEEKLY:
        return resample_daily_to_weekly(rows)
    elif timeframe == RegimeTimeframe.MONTHLY:
        return resample_daily_to_monthly(rows)
    else:
        # For UNKNOWN or CUSTOM, just return normalized
        return normalize_ohlcv_rows(rows)

def resample_daily_to_weekly(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = normalize_ohlcv_rows(rows)
    if not rows:
        return []

    df = rows_to_dataframe_safe(rows)
    # Resample to weekly (W-FRI)
    resampled = df.resample('W-FRI').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    resampled.dropna(inplace=True)
    return dataframe_to_ohlcv_rows(resampled)

def resample_daily_to_monthly(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = normalize_ohlcv_rows(rows)
    if not rows:
        return []

    df = rows_to_dataframe_safe(rows)
    # Resample to monthly (M)
    resampled = df.resample('ME').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    resampled.dropna(inplace=True)
    return dataframe_to_ohlcv_rows(resampled)

def timeframe_resample_summary(rows: list[dict[str, Any]], resampled: list[dict[str, Any]], timeframe: RegimeTimeframe) -> dict[str, Any]:
    return {
        "original_count": len(rows),
        "resampled_count": len(resampled),
        "target_timeframe": timeframe.value
    }

def timeframe_resample_summary_to_text(summary: dict[str, Any]) -> str:
    return (f"Timeframe Resampler Summary:\n"
            f"Original Rows: {summary['original_count']}\n"
            f"Target Timeframe: {summary['target_timeframe']}\n"
            f"Resampled Rows: {summary['resampled_count']}")
