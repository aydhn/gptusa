from typing import Any
import pandas

def validate_closure_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_closure_columns(columns)

def validate_no_forbidden_closure_columns(columns: list[str]) -> list[str]:
    errors = []
    forbidden = [
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "order", "broker_order", "paper_order", "live_order", "live_signal", "buy_signal", "sell_signal"
    ]
    for col in columns:
        if any(f in col.lower() for f in forbidden):
            errors.append(f"Forbidden column name detected: {col}")
    return errors

def closure_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def closure_schema_to_text(errors: list[str]) -> str:
    return "Valid" if not errors else f"Invalid: {', '.join(errors)}"
