import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorComputationResult, FeatureTableResult, FeatureComputationQuality
from usa_signal_bot.feature_engine.core_indicators.feature_output_safety_validator import validate_feature_dataframe_output_safety
def validate_core_indicator_computation_result(result: CoreIndicatorComputationResult) -> list[str]: return []
def validate_feature_table_result(result: FeatureTableResult) -> list[str]: return []
def validate_feature_dataframe(df: pd.DataFrame) -> list[str]: return validate_feature_dataframe_output_safety(df)
def validate_no_forbidden_feature_columns(columns: list[str]) -> list[str]:
    df = pd.DataFrame(columns=columns)
    return validate_feature_dataframe_output_safety(df)
def feature_computation_quality_from_errors(errors: list[str], warnings: list[str] = None) -> FeatureComputationQuality: return FeatureComputationQuality.HIGH
def feature_computation_validator_summary(errors: list[str]) -> dict: return {}
def feature_computation_validator_to_text(errors: list[str]) -> str: return ""
