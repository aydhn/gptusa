from typing import Any
from usa_signal_bot.regime_classification.validation.phase132_models import (
    CompatibilityValidationResult,
    ConditionalDiagnosticResult,
    RegimeAwareAcceptanceGate
)

FORBIDDEN_COLUMNS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch"
]

def validate_compatibility_validation_result_schema(result: CompatibilityValidationResult) -> list[str]:
    errors = []
    if not result.validation_id:
        errors.append("Missing validation_id")
    if not result.research_metadata_only:
        errors.append("research_metadata_only must be true")
    return errors

def validate_conditional_diagnostic_schema(result: ConditionalDiagnosticResult) -> list[str]:
    errors = []
    if not result.diagnostic_id:
        errors.append("Missing diagnostic_id")
    return errors

def validate_acceptance_gate_schema(gate: RegimeAwareAcceptanceGate) -> list[str]:
    errors = []
    if not gate.gate_id:
        errors.append("Missing gate_id")
    return errors

def validate_context_validation_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_context_validation_columns(columns)

def validate_no_forbidden_context_validation_columns(columns: list[str]) -> list[str]:
    errors = []
    for col in columns:
        col_lower = col.lower()
        for forbidden in FORBIDDEN_COLUMNS:
            if forbidden in col_lower:
                errors.append(f"Forbidden column name found: {col}")
        # 'signal' exception
        if "signal" in col_lower and col_lower != "macd_signal_9":
            errors.append(f"Forbidden column name found: {col} (contains 'signal')")
    return errors

def compatibility_validation_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def compatibility_validation_schema_to_text(errors: list[str]) -> str:
    if not errors:
        return "Schema validation passed."
    return f"Schema validation failed with {len(errors)} errors.\n" + "\n".join(errors[:5])
