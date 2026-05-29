import pandas as pd
from typing import Any

def validate_no_forbidden_regime_label_columns(columns: list[str]) -> list[str]:
    errors = []
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper",
        "live", "demo_order", "live_order", "sent_to_broker",
        "deploy", "production_patch"
    ]

    for col in columns:
        col_lower = col.lower()
        if "signal" in col_lower and col_lower != "macd_signal_9":
            errors.append(f"Forbidden column name containing 'signal': {col}")

        for frag in forbidden_fragments:
            if frag in col_lower:
                errors.append(f"Forbidden column name containing '{frag}': {col}")

    return errors

def validate_regime_label_result_columns(columns: list[str]) -> list[str]:
    errors = validate_no_forbidden_regime_label_columns(columns)

    required = ["regime_label_research", "regime_label_confidence"]
    for r in required:
        if r not in columns:
            errors.append(f"Missing required output column: {r}")

    return errors

def validate_regime_label_dataframe_schema(df: pd.DataFrame) -> list[str]:
    return validate_regime_label_result_columns(df.columns.tolist())

def validate_regime_label_values(labels: list[str]) -> list[str]:
    errors = []
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "portfolio"
    ]

    valid_labels = [l for l in labels if pd.notna(l)]
    unique = set(valid_labels)

    for val in unique:
        val_lower = str(val).lower()
        if "signal" in val_lower:
            errors.append(f"Forbidden label value containing 'signal': {val}")

        for frag in forbidden_fragments:
            if frag in val_lower:
                errors.append(f"Forbidden label value containing '{frag}': {val}")

    return errors

def regime_label_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def regime_label_schema_to_text(errors: list[str]) -> str:
    if not errors:
        return "Schema is valid"
    return f"Schema invalid. {len(errors)} errors: {', '.join(errors[:3])}"
