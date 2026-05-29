import pandas as pd
from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import RegimeDiagnosticsSchemaValidationError
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionAnalyticsResult,
    RegimeTransitionMatrix
)
from usa_signal_bot.regime_classification.diagnostics.regime_sequence_input_loader import FORBIDDEN_COLUMNS

def validate_no_forbidden_regime_diagnostics_columns(columns: List[str]) -> List[str]:
    errors = []
    for col in columns:
        cl = col.lower()
        if "macd_signal_9" in cl:
            continue
        for f in FORBIDDEN_COLUMNS:
            if f in cl:
                errors.append(f"Forbidden column: {col} contains '{f}'")
    return errors

def validate_regime_diagnostics_column_names(columns: List[str]) -> List[str]:
    errors = []
    if "regime_label_research" not in columns:
        errors.append("Missing required column 'regime_label_research'")
    errors.extend(validate_no_forbidden_regime_diagnostics_columns(columns))
    return errors

def validate_regime_diagnostics_dataframe_schema(df: pd.DataFrame) -> List[str]:
    return validate_regime_diagnostics_column_names(list(df.columns))

def validate_transition_matrix_schema(matrix: RegimeTransitionMatrix) -> List[str]:
    errors = []
    if not matrix.matrix_valid:
        errors.append("Matrix is not valid.")
    return errors

def validate_analytics_result_schema(result: RegimeTransitionAnalyticsResult) -> List[str]:
    errors = []
    if not result.analytics_valid:
        errors.append("Analytics result is marked invalid.")
    return errors

def regime_diagnostics_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors), "valid": len(errors) == 0}

def regime_diagnostics_schema_to_text(errors: List[str]) -> str:
    if not errors:
        return "Schema valid."
    return "Schema errors:\n" + "\n".join([f" - {e}" for e in errors])
