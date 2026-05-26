import pandas as pd
from typing import List, Dict, Any, Optional
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureContext,
    AdvancedFeatureComputationResult,
    AdvancedFeatureTableResult,
    AdvancedFeatureRiskFlag
)

def validate_advanced_feature_context_safety(context: AdvancedFeatureContext) -> List[str]:
    errors = []
    if context.activation_allowed:
        errors.append("Context activation_allowed is True.")
    if context.active_paper_enabled:
        errors.append("Context active_paper_enabled is True.")
    if context.broker_execution_enabled:
        errors.append("Context broker_execution_enabled is True.")
    if context.order_creation_enabled:
        errors.append("Context order_creation_enabled is True.")
    if context.paper_state_mutation_enabled:
        errors.append("Context paper_state_mutation_enabled is True.")
    if context.telegram_real_send_enabled:
        errors.append("Context telegram_real_send_enabled is True.")
    if context.produces_trade_signal:
        errors.append("Context produces_trade_signal is True.")
    if context.produces_portfolio_weights:
        errors.append("Context produces_portfolio_weights is True.")
    if context.network_used or context.paid_api_used or context.broker_used:
        errors.append("Context shows network, paid API, or broker was used.")

    return errors

def validate_advanced_feature_results_safety(results: List[AdvancedFeatureComputationResult]) -> List[str]:
    errors = []
    for r in results:
        if r.produced_trade_signal or r.produced_order_decision or r.produced_portfolio_weights:
            errors.append(f"Result {r.result_id} produced execution signals/weights.")
        if r.broker_used or r.paper_state_mutated or r.network_used:
            errors.append(f"Result {r.result_id} violated isolation boundaries.")
    return errors

def validate_advanced_feature_table_safety(table: AdvancedFeatureTableResult) -> List[str]:
    errors = []
    if table.produced_trade_signal or table.produced_portfolio_weights:
        errors.append(f"Table {table.table_id} for {table.symbol} contains signal/weight intent.")
    return errors

def validate_advanced_feature_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    from usa_signal_bot.feature_engine.advanced_features.advanced_feature_schema import validate_advanced_feature_column_names
    return validate_advanced_feature_column_names(list(df.columns))

def advanced_feature_output_text_has_trade_or_execution_language(text: str) -> bool:
    text_lower = text.lower()
    forbidden_phrases = [
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "canlıya alındı", "kesin al", "kesin sat", "garanti kâr",
        "buy signal", "sell signal", "strong buy", "strong sell",
        "live order", "sent to broker"
    ]
    for phrase in forbidden_phrases:
        if phrase in text_lower:
            return True
    return False

def collect_advanced_feature_risk_flags(context: Optional[AdvancedFeatureContext] = None) -> List[AdvancedFeatureRiskFlag]:
    flags = []
    if context:
        if not context.source_core_indicator_review_id:
            flags.append(AdvancedFeatureRiskFlag.CORE_INDICATOR_REVIEW_MISSING)
        if context.produces_trade_signal:
            flags.append(AdvancedFeatureRiskFlag.TRADE_SIGNAL_COLUMN_RISK)
    return flags

def advanced_feature_output_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def advanced_feature_output_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Output Safety: PASSED. No execution logic detected."
    return "OUTPUT SAFETY VIOLATION:\n" + "\n".join(errors)
