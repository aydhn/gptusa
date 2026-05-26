import pandas as pd
from typing import List, Dict, Any

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "paper", "live", "demo_order",
    "live_order", "sent_to_broker"
]
# "signal" is partially forbidden unless inherited from phase 117 (macd_signal_9)

def validate_advanced_feature_column_names(columns: List[str]) -> List[str]:
    errors = []
    for col in columns:
        col_lower = col.lower()
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in col_lower:
                errors.append(f"Forbidden fragment '{frag}' found in column '{col}'.")

        # Specific check for signal
        if "signal" in col_lower and not col_lower.startswith("macd_signal"):
            errors.append(f"Forbidden fragment 'signal' found in column '{col}' (not macd_signal whitelist).")

    return errors

def validate_advanced_feature_table_schema(df: pd.DataFrame) -> List[str]:
    return validate_advanced_feature_column_names(list(df.columns))

def validate_multi_symbol_advanced_schema(tables: Dict[str, pd.DataFrame]) -> List[str]:
    errors = []
    for sym, df in tables.items():
        sym_errs = validate_advanced_feature_table_schema(df)
        if sym_errs:
            errors.extend([f"[{sym}] {e}" for e in sym_errs])
    return errors

def advanced_feature_schema_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    errors = validate_multi_symbol_advanced_schema(tables)
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def advanced_feature_schema_to_text(errors: List[str]) -> str:
    if not errors:
        return "Schema is safe. No forbidden execution columns detected."
    return "SCHEMA VIOLATION:\n" + "\n".join(errors)
