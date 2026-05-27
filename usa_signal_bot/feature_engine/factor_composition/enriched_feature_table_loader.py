from typing import Any
from pathlib import Path
import pandas as pd
import os

def load_enriched_feature_table_csv(path: Path) -> pd.DataFrame:
    # Anti-path traversal
    real_path = os.path.realpath(str(path))
    if not os.path.exists(real_path):
        raise FileNotFoundError(f"CSV file not found: {real_path}")

    df = pd.read_csv(real_path)
    return df

def load_enriched_feature_tables(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    tables = {}
    for symbol, path in paths.items():
        tables[symbol] = load_enriched_feature_table_csv(path)
    return tables

def validate_enriched_feature_table_input(df: pd.DataFrame) -> list[str]:
    errors = []

    if 'symbol' not in df.columns:
        errors.append("Missing required 'symbol' column")
    if 'timestamp' not in df.columns:
        errors.append("Missing required 'timestamp' column")

    forbidden_columns = ["buy_signal", "sell_signal", "entry", "exit", "position", "order", "portfolio_weight", "target_weight", "broker_order_id", "real_fill_id", "active_trading_signal"]

    for col in df.columns:
        for forbidden in forbidden_columns:
            if forbidden in col.lower() and "macd_signal" not in col.lower():
                errors.append(f"Forbidden column detected: {col}")

    return errors

def validate_enriched_feature_tables(tables: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    for symbol, df in tables.items():
        table_errors = validate_enriched_feature_table_input(df)
        if table_errors:
            errors.append(f"Errors in table for {symbol}: {', '.join(table_errors)}")
    return errors

def enriched_feature_table_loader_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    summary = {
        "table_count": len(tables),
        "symbols": list(tables.keys()),
        "rows_by_symbol": {sym: len(df) for sym, df in tables.items()},
        "columns_by_symbol": {sym: len(df.columns) for sym, df in tables.items()}
    }
    return summary

def enriched_feature_table_loader_to_text(tables: dict[str, pd.DataFrame], limit: int = 50) -> str:
    lines = ["Enriched Feature Tables Summary:"]
    summary = enriched_feature_table_loader_summary(tables)
    lines.append(f"  Loaded Tables: {summary['table_count']}")
    lines.append(f"  Symbols: {', '.join(summary['symbols'][:limit])}")
    for sym, count in summary['rows_by_symbol'].items():
        lines.append(f"    {sym}: {count} rows, {summary['columns_by_symbol'][sym]} columns")
    return "\n".join(lines)
