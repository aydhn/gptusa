import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeSequenceInputLoaderError

FORBIDDEN_COLUMNS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch"
]

def load_labeled_regime_table_csv(path: Path) -> pd.DataFrame:
    path_str = str(path)
    if ".." in path_str or not path.is_file():
        raise RegimeSequenceInputLoaderError(f"Invalid or missing CSV path: {path}")

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise RegimeSequenceInputLoaderError(f"Failed to read CSV at {path}: {e}")

def load_labeled_regime_tables(paths: Dict[str, Path]) -> Dict[str, pd.DataFrame]:
    tables = {}
    for symbol, path in paths.items():
        tables[symbol] = load_labeled_regime_table_csv(path)
    return tables

def load_regime_label_sequences_jsonl(path: Path) -> List[Dict[str, Any]]:
    if ".." in str(path) or not path.is_file():
        raise RegimeSequenceInputLoaderError(f"Invalid JSONL path: {path}")

    sequences = []
    try:
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    sequences.append(json.loads(line))
    except Exception as e:
        raise RegimeSequenceInputLoaderError(f"Failed to read JSONL at {path}: {e}")
    return sequences

def validate_labeled_regime_table(df: pd.DataFrame) -> List[str]:
    errors = []
    cols = [c.lower() for c in df.columns]

    for fcol in FORBIDDEN_COLUMNS:
        for c in cols:
            if fcol in c and c != "macd_signal_9":
                errors.append(f"Forbidden column detected: {c}")

    if "regime_label_research" not in df.columns:
        errors.append("Missing required column 'regime_label_research'")

    return errors

def validate_labeled_regime_tables(tables: Dict[str, pd.DataFrame]) -> List[str]:
    errors = []
    for symbol, df in tables.items():
        errs = validate_labeled_regime_table(df)
        for e in errs:
            errors.append(f"[{symbol}] {e}")
    return errors

def infer_regime_label_column(df: pd.DataFrame) -> Optional[str]:
    if "regime_label_research" in df.columns:
        return "regime_label_research"
    for col in df.columns:
        if "label" in col.lower() and "regime" in col.lower():
            return col
    return None

def infer_regime_confidence_column(df: pd.DataFrame) -> Optional[str]:
    if "regime_label_confidence" in df.columns:
        return "regime_label_confidence"
    for col in df.columns:
        if "confidence" in col.lower() and "regime" in col.lower():
            return col
    return None

def regime_sequence_input_loader_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    summary = {
        "table_count": len(tables),
        "total_rows": sum(len(df) for df in tables.values()),
        "symbols": list(tables.keys()),
        "validation_errors": validate_labeled_regime_tables(tables)
    }
    return summary

def regime_sequence_input_loader_to_text(tables: Dict[str, pd.DataFrame], limit: int = 100) -> str:
    summary = regime_sequence_input_loader_summary(tables)
    lines = [
        "Regime Sequence Input Loader Summary",
        f"Tables Loaded: {summary['table_count']}",
        f"Total Rows: {summary['total_rows']}",
        f"Symbols: {', '.join(summary['symbols'])}"
    ]
    if summary["validation_errors"]:
        lines.append("Validation Errors:")
        for e in summary["validation_errors"]:
            lines.append(f" - {e}")
    return "\n".join(lines)
