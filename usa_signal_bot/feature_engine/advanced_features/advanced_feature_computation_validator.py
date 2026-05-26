import pandas as pd
from typing import List, Dict, Any, Optional
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureComputationResult,
    AdvancedFeatureTableResult,
    AdvancedFeatureQuality
)
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_schema import validate_advanced_feature_column_names

def validate_advanced_feature_computation_result(result: AdvancedFeatureComputationResult) -> List[str]:
    errors = []
    if result.produced_trade_signal:
        errors.append("Result indicates trade signal was produced.")
    if result.produced_order_decision:
        errors.append("Result indicates order decision was produced.")
    if result.produced_portfolio_weights:
        errors.append("Result indicates portfolio weights were produced.")
    if result.network_used or result.broker_used or result.paper_state_mutated:
        errors.append("Result indicates network, broker, or paper mutation occurred.")
    return errors

def validate_advanced_feature_table_result(result: AdvancedFeatureTableResult) -> List[str]:
    errors = []
    if result.produced_trade_signal:
        errors.append("Table result indicates trade signal was produced.")
    if result.produced_order_decision:
        errors.append("Table result indicates order decision was produced.")
    if result.produced_portfolio_weights:
        errors.append("Table result indicates portfolio weights were produced.")

    schema_errs = validate_advanced_feature_column_names(result.columns)
    errors.extend(schema_errs)

    return errors

def validate_advanced_feature_dataframe(df: pd.DataFrame) -> List[str]:
    return validate_advanced_feature_column_names(list(df.columns))

def validate_no_forbidden_advanced_feature_columns(columns: List[str]) -> List[str]:
    return validate_advanced_feature_column_names(columns)

def advanced_feature_quality_from_errors(errors: List[str], warnings: Optional[List[str]] = None) -> AdvancedFeatureQuality:
    if errors:
        return AdvancedFeatureQuality.INVALID
    if warnings:
        return AdvancedFeatureQuality.WARNING
    return AdvancedFeatureQuality.HIGH

def advanced_feature_computation_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def advanced_feature_computation_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Computation result is safe."
    return "COMPUTATION VIOLATION:\n" + "\n".join(errors)
