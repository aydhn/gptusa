from typing import Any
import pandas as pd

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringResult,
    FactorTableResult,
    FactorScoreQuality,
    validate_factor_scoring_result as base_validate_result,
    validate_factor_table_result as base_validate_table
)

def validate_factor_scoring_result(result: FactorScoringResult) -> list[str]:
    errors = []
    try:
        base_validate_result(result)
    except Exception as e:
        errors.append(str(e))
    return errors

def validate_factor_table_result(result: FactorTableResult) -> list[str]:
    errors = []
    try:
        base_validate_table(result)
    except Exception as e:
        errors.append(str(e))
    return errors

def validate_factor_dataframe(df: pd.DataFrame) -> list[str]:
    errors = []
    from usa_signal_bot.feature_engine.factor_scoring.factor_table_schema import validate_no_forbidden_factor_columns
    errs = validate_no_forbidden_factor_columns(list(df.columns))
    errors.extend(errs)
    return errors

def validate_factor_table_outputs(tables: dict[str, pd.DataFrame]) -> list[str]:
    errors = []
    for sym, df in tables.items():
        errs = validate_factor_dataframe(df)
        errors.extend([f"[{sym}] {e}" for e in errs])
    return errors

def factor_score_quality_from_errors(errors: list[str], warnings: list[str] | None = None) -> FactorScoreQuality:
    if errors:
        return FactorScoreQuality.INVALID
    if warnings:
        return FactorScoreQuality.WARNING
    return FactorScoreQuality.ACCEPTABLE

def factor_computation_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"status": "ok"}

def factor_computation_validator_to_text(errors: list[str]) -> str:
    return f"Errors: {len(errors)}"
