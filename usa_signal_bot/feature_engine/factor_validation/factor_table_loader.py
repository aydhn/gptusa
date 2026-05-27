import pandas as pd
from pathlib import Path
from typing import Any

def load_factor_table_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception as e:
        return pd.DataFrame()

def load_factor_tables(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    res = {}
    for sym, path in paths.items():
        res[sym] = load_factor_table_csv(path)
    return res

def validate_factor_table_input(df: pd.DataFrame) -> list[str]:
    errors = []
    if df.empty:
        errors.append("DataFrame is empty")
    return errors

def validate_factor_tables_input(tables: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    for sym, df in tables.items():
        errors.extend(validate_factor_table_input(df))
    return errors

def factor_columns_from_table(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in ['symbol', 'timestamp', 'date', 'datetime']]

def factor_table_loader_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    return {"loaded_tables": len(tables)}

def factor_table_loader_to_text(tables: dict[str, pd.DataFrame], limit: int = 50) -> str:
    return f"Loaded {len(tables)} tables."
