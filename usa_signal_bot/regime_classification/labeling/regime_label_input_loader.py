import pandas as pd
from pathlib import Path
from typing import Any
import json
from usa_signal_bot.core.exceptions import RegimeLabelInputLoaderError

def load_regime_feature_table_csv(path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise RegimeLabelInputLoaderError(f"Failed to load CSV from {path}: {str(e)}")

def load_regime_feature_tables(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    tables = {}
    for symbol, path in paths.items():
        # Prevent path traversal
        resolved = path.resolve()
        # Basic check to avoid arbitrary reads
        if ".." in str(path):
            raise RegimeLabelInputLoaderError(f"Path traversal detected: {path}")

        tables[symbol] = load_regime_feature_table_csv(resolved)
    return tables

def load_candidate_scores_jsonl(path: Path) -> list[dict[str, Any]]:
    scores = []
    try:
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    scores.append(json.loads(line))
        return scores
    except Exception as e:
        raise RegimeLabelInputLoaderError(f"Failed to load candidate scores from {path}: {str(e)}")

def load_candidate_definitions_jsonl(path: Path) -> list[dict[str, Any]]:
    defs = []
    try:
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    defs.append(json.loads(line))
        return defs
    except Exception as e:
        raise RegimeLabelInputLoaderError(f"Failed to load candidate definitions from {path}: {str(e)}")

def validate_regime_label_input_table(df: pd.DataFrame) -> list[str]:
    errors = []
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper",
        "live", "demo_order", "live_order", "sent_to_broker",
        "deploy", "production_patch"
    ]

    # "signal" is forbidden unless it's "macd_signal_9"

    for col in df.columns:
        col_lower = col.lower()
        if "signal" in col_lower and col_lower != "macd_signal_9":
            errors.append(f"Forbidden column name containing 'signal': {col}")

        for frag in forbidden_fragments:
            if frag in col_lower:
                errors.append(f"Forbidden column name containing '{frag}': {col}")

    if "symbol" not in df.columns and "timestamp" not in df.columns and "date" not in df.columns:
        errors.append("Table missing standard identifier columns (symbol, timestamp/date)")

    return errors

def validate_regime_label_input_tables(tables: dict[str, pd.DataFrame]) -> list[str]:
    all_errors = []
    for symbol, df in tables.items():
        errors = validate_regime_label_input_table(df)
        all_errors.extend([f"[{symbol}] {e}" for e in errors])
    return all_errors

def infer_candidate_score_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col.startswith("score_") or col.endswith("_score")]

def regime_label_input_loader_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    return {
        "table_count": len(tables),
        "symbols": list(tables.keys()),
        "total_rows": sum(len(df) for df in tables.values())
    }

def regime_label_input_loader_to_text(tables: dict[str, pd.DataFrame], limit: int = 100) -> str:
    summary = regime_label_input_loader_summary(tables)
    return f"Loaded {summary['table_count']} tables for symbols: {', '.join(summary['symbols'])} (Total rows: {summary['total_rows']})"
