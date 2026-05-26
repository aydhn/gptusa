import pandas as pd
from typing import List
from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorContext, CoreIndicatorRiskFlag
from usa_signal_bot.feature_engine.core_indicators.feature_table_builder import feature_columns_from_dataframe

def feature_output_text_has_trade_or_execution_language(text: str) -> bool:
    dangerous = ["emir gönderildi", "buy signal", "sell signal"]
    return any(d in text.lower() for d in dangerous)

def validate_no_forbidden_feature_columns(columns: List[str]) -> List[str]:
    errors = []
    block_words = ["buy", "sell", "entry", "exit", "order", "broker", "position", "paper", "live"]
    for c in columns:
        if c.lower() == "macd_signal_9": continue
        if any(w in c.lower() for w in block_words):
            errors.append(f"Forbidden column name detected: {c}")
    return errors

def validate_feature_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return validate_no_forbidden_feature_columns(list(df.columns))

def validate_core_indicator_context_safety(context: CoreIndicatorContext) -> List[str]:
    return []

def collect_core_indicator_risk_flags(context=None) -> List[CoreIndicatorRiskFlag]:
    return []
