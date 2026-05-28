try:
    import pandas as pd
except ImportError:
    pass
from pathlib import Path
from typing import Any
import json

FORBIDDEN_COLUMNS = ["buy", "sell", "entry", "exit", "order", "broker", "portfolio_weight"]

def load_frozen_factor_table_csv(path: Path):
    return pd.read_csv(path)

def load_frozen_factor_tables(paths: dict[str, Path]):
    return {s: load_frozen_factor_table_csv(p) for s, p in paths.items()}

def validate_market_state_input_table(df) -> list[str]:
    errors = []
    cols = [str(c).lower() for c in df.columns]
    if "symbol" not in cols:
        errors.append("Missing symbol")
    for c in cols:
        for f in FORBIDDEN_COLUMNS:
            if f in c:
                errors.append(f"Forbidden column: {c}")
    return errors

def validate_market_state_input_tables(tables) -> list[str]:
    return [e for s, df in tables.items() for e in validate_market_state_input_table(df)]
