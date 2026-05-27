from pathlib import Path
from typing import Any
import pandas as pd

from usa_signal_bot.core.exceptions import FactorTableInputLoaderError

def load_factor_input_table_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FactorTableInputLoaderError(f"Input path not found: {path}")

    str_path = str(path)
    if ".." in str_path or "~" in str_path:
        raise FactorTableInputLoaderError(f"Path traversal not allowed: {path}")

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise FactorTableInputLoaderError(f"Failed to load CSV: {e}")

def load_factor_input_tables(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    tables = {}
    for symbol, path in paths.items():
        tables[symbol] = load_factor_input_table_csv(path)
    return tables

def validate_factor_input_table(df: pd.DataFrame) -> list[str]:
    errors = []
    if df.empty:
        errors.append("Input table is empty")

    columns = set(df.columns)
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper",
        "live", "demo_order", "live_order", "sent_to_broker"
    ]

    for col in columns:
        col_lower = col.lower()
        if "macd_signal" in col_lower:
            continue
        if "signal" in col_lower:
             errors.append(f"Forbidden column contains 'signal': {col}")
        for frag in forbidden_fragments:
            if frag in col_lower:
                errors.append(f"Forbidden column contains '{frag}': {col}")

    if "symbol" not in columns:
        errors.append("Missing required column 'symbol'")
    if "timestamp" not in columns:
        errors.append("Missing required column 'timestamp'")

    return errors

def validate_factor_input_tables(tables: dict[str, pd.DataFrame]) -> list[str]:
    all_errors = []
    for symbol, df in tables.items():
        errors = validate_factor_input_table(df)
        all_errors.extend([f"[{symbol}] {e}" for e in errors])
    return all_errors

def factor_input_table_loader_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    return {
        "symbols": list(tables.keys()),
        "table_count": len(tables),
        "total_rows": sum(len(df) for df in tables.values())
    }

def factor_input_table_loader_to_text(tables: dict[str, pd.DataFrame], limit: int = 50) -> str:
    summary = factor_input_table_loader_summary(tables)
    lines = [
        "--- Factor Input Table Loader ---",
        f"Loaded {summary['table_count']} tables",
        f"Total rows: {summary['total_rows']}"
    ]
    return "\n".join(lines)
