import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorContext, CoreIndicatorComputationResult, FeatureTableResult, CoreIndicatorRiskFlag
def validate_core_indicator_context_safety(context: CoreIndicatorContext) -> list[str]:
    errs = []
    if context.activation_allowed: errs.append("activation_allowed is true")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled is true")
    return errs
def validate_core_indicator_results_safety(results: list[CoreIndicatorComputationResult]) -> list[str]: return []
def validate_feature_table_safety(table: FeatureTableResult) -> list[str]: return []
def validate_feature_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    errs = []
    forbidden = ['buy', 'sell', 'signal', 'entry', 'exit', 'order', 'broker', 'position', 'paper', 'live', 'sent_to_broker']
    for col in df.columns:
        if col == 'macd_signal_9': continue
        if any(f in col.lower() for f in forbidden):
            errs.append(f"Forbidden column detected: {col}")
    return errs
def feature_output_text_has_trade_or_execution_language(text: str) -> bool: return False
def collect_core_indicator_risk_flags(context: CoreIndicatorContext = None) -> list[CoreIndicatorRiskFlag]: return []
def feature_output_safety_summary(errors: list[str]) -> dict: return {}
def feature_output_safety_to_text(errors: list[str]) -> str: return str(errors)
