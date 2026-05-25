from pathlib import Path
from typing import Any, Dict, List
import pandas as pd

def sample_ohlcv_records(symbol: str = "AAPL", rows: int = 5) -> List[Dict[str, Any]]:
    records = []
    base_price = 150.0
    for i in range(rows):
        records.append({
            "symbol": symbol,
            "timestamp": f"2023-01-0{i+1}T00:00:00Z",
            "open": base_price + i,
            "high": base_price + i + 2,
            "low": base_price + i - 1,
            "close": base_price + i + 1,
            "adjusted_close": base_price + i + 1,
            "volume": 1000000 + (i * 10000)
        })
    return records

def sample_ohlcv_dataframe(symbol: str = "AAPL", rows: int = 5) -> pd.DataFrame:
    records = sample_ohlcv_records(symbol, rows)
    return pd.DataFrame(records)

def malformed_ohlcv_records_missing_close() -> List[Dict[str, Any]]:
    return [
        {
            "symbol": "AAPL",
            "timestamp": "2023-01-01T00:00:00Z",
            "open": 150.0,
            "high": 152.0,
            "low": 149.0,
            # close missing
            "volume": 1000000
        }
    ]

def empty_ohlcv_dataframe() -> pd.DataFrame:
    return pd.DataFrame()

def write_sample_ohlcv_csv(path: Path, symbol: str = "AAPL", rows: int = 5) -> Path:
    df = sample_ohlcv_dataframe(symbol, rows)
    df.to_csv(path, index=False)
    return path
