from typing import List
import pandas as pd
import numpy as np

from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.features.output_contract import FeatureRow
from usa_signal_bot.core.exceptions import FeatureComputationError

def bars_to_dataframe(bars: List[OHLCVBar]) -> pd.DataFrame:
    if not bars:
        return pd.DataFrame()

    records = []
    for b in bars:
        rec = {
            "timestamp_utc": b.timestamp_utc,
            "open": b.open,
            "high": b.high,
            "low": b.low,
            "close": b.close,
            "volume": b.volume
        }
        if b.adjusted_close is not None:
            rec["adjusted_close"] = b.adjusted_close
        records.append(rec)

    df = pd.DataFrame.from_records(records)
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    df = df.sort_values("timestamp_utc").reset_index(drop=True)
    df["timestamp_utc"] = df["timestamp_utc"].apply(lambda x: x.isoformat())
    return df

def dataframe_to_feature_rows(df: pd.DataFrame, symbol: str, timeframe: str) -> List[FeatureRow]:
    if df.empty:
        return []

    rows = []
    feature_cols = [c for c in df.columns if c not in ["timestamp_utc", "symbol", "timeframe"]]

    df_clean = df.replace({np.nan: None})

    for _, row in df_clean.iterrows():
        features = {col: row[col] for col in feature_cols}
        rows.append(FeatureRow(
            timestamp_utc=row["timestamp_utc"],
            symbol=symbol,
            timeframe=timeframe,
            features=features
        ))
    return rows

def ensure_ohlcv_dataframe_columns(df: pd.DataFrame) -> None:
    required = ["timestamp_utc", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise FeatureComputationError(f"DataFrame is missing required OHLCV columns: {missing}")

def sort_ohlcv_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp_utc" not in df.columns:
        return df

    temp_time = pd.to_datetime(df["timestamp_utc"], utc=True)
    df = df.iloc[temp_time.argsort()].reset_index(drop=True)
    return df

def add_symbol_timeframe_columns(df: pd.DataFrame, symbol: str, timeframe: str) -> pd.DataFrame:
    df["symbol"] = symbol
    df["timeframe"] = timeframe
    return df

def normalize_feature_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [c for c in df.columns if c not in ["timestamp_utc", "symbol", "timeframe"]]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
