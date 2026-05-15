from typing import Any
import pandas as pd
from usa_signal_bot.core.enums import RegimeTimeframe


def normalize_ohlcv_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    df = rows_to_dataframe_safe(rows)
    df.sort_values('date', inplace=True)
    return dataframe_to_ohlcv_rows(df)

def rows_to_dataframe_safe(rows: list[dict[str, Any]]) -> Any:
    if not rows:
        return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df = pd.DataFrame(rows)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], utc=True)
    return df

def dataframe_to_ohlcv_rows(df: Any) -> list[dict[str, Any]]:
    if df.empty:
        return []

    records = df.copy()
    if 'date' in records.columns:
        records['date'] = records['date'].dt.strftime('%Y-%m-%d')
    return records.to_dict('records')

def resample_ohlcv_rows(rows: list[dict[str, Any]], timeframe: RegimeTimeframe) -> list[dict[str, Any]]:
    if not rows:
        return []

    if timeframe == RegimeTimeframe.DAILY:
        return normalize_ohlcv_rows(rows)
    elif timeframe == RegimeTimeframe.WEEKLY:
        return resample_daily_to_weekly(rows)
    elif timeframe == RegimeTimeframe.MONTHLY:
        return resample_daily_to_monthly(rows)

    return normalize_ohlcv_rows(rows)

def resample_daily_to_weekly(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []

    df = rows_to_dataframe_safe(rows)
    df.set_index('date', inplace=True)

    resampled = df.resample('W-FRI').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    resampled.reset_index(inplace=True)
    return dataframe_to_ohlcv_rows(resampled)

def resample_daily_to_monthly(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
     if not rows:
        return []

     df = rows_to_dataframe_safe(rows)
     df.set_index('date', inplace=True)

     resampled = df.resample('M').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

     resampled.reset_index(inplace=True)
     return dataframe_to_ohlcv_rows(resampled)

def timeframe_resample_summary(rows: list[dict[str, Any]], resampled: list[dict[str, Any]], timeframe: RegimeTimeframe) -> dict[str, Any]:
    return {
        "original_count": len(rows),
        "resampled_count": len(resampled),
        "timeframe": timeframe.value
    }

def timeframe_resample_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Resampled {summary['original_count']} rows to {summary['resampled_count']} {summary['timeframe']} rows."
