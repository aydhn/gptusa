import pandas as pd
from typing import Any

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "paper", "live", "demo_order",
    "live_order", "sent_to_broker"
]

def validate_interaction_column_names(columns: list[str]) -> list[str]:
    errors = []
    for col in columns:
        col_lower = col.lower()
        if "signal" in col_lower and col_lower != "macd_signal_9":
            errors.append(f"Forbidden column: {col}")
            continue
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in col_lower:
                errors.append(f"Forbidden column: {col}")
                break
    return errors

def validate_interaction_dataframe_schema(df: pd.DataFrame) -> list[str]:
    return validate_interaction_column_names(list(df.columns))

def validate_no_forbidden_interaction_columns(columns: list[str]) -> list[str]:
    return validate_interaction_column_names(columns)

def interaction_schema_summary(df: pd.DataFrame) -> dict[str, Any]:
    return {"errors": validate_interaction_dataframe_schema(df)}

def interaction_schema_to_text(errors: list[str]) -> str:
    if not errors:
        return "Valid schema"
    return "\n".join(errors)
