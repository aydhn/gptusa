import pandas as pd
from pathlib import Path
def load_ohlcv_feature_input_csv(path: Path) -> list[dict]:
    df = pd.read_csv(path)
    return dataframe_to_records(df)
def records_to_dataframe(records: list[dict]) -> pd.DataFrame: return pd.DataFrame(records)
def dataframe_to_records(df: pd.DataFrame) -> list[dict]: return df.to_dict('records')
def validate_ohlcv_feature_input(records: list[dict]) -> list[str]:
    df = pd.DataFrame(records)
    errs = []
    if not {'symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume'}.issubset(df.columns): errs.append("Missing required OHLCV columns")
    return errs
def sort_ohlcv_by_symbol_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    if 'symbol' in df.columns and 'timestamp' in df.columns: return df.sort_values(['symbol', 'timestamp']).reset_index(drop=True)
    return df
def ohlcv_feature_input_summary(records: list[dict]) -> dict: return {}
def ohlcv_feature_input_to_text(records: list[dict], limit: int = 20) -> str: return ""
