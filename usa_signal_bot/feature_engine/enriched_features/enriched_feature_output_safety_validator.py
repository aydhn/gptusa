import pandas as pd
from typing import Any
from usa_signal_bot.core.enums import FeatureEnrichmentRiskFlag
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureEnrichmentContext,
    FeatureEnrichmentResult,
    EnrichedFeatureTableResult
)
from usa_signal_bot.feature_engine.enriched_features.interaction_schema_validator import FORBIDDEN_FRAGMENTS

def validate_feature_enrichment_context_safety(context: FeatureEnrichmentContext) -> list[str]:
    errors = []
    if context.activation_allowed: errors.append("activation_allowed is true")
    if context.active_paper_enabled: errors.append("active_paper_enabled is true")
    if context.broker_execution_enabled: errors.append("broker_execution_enabled is true")
    if context.order_creation_enabled: errors.append("order_creation_enabled is true")
    if context.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled: errors.append("telegram_real_send_enabled is true")
    if context.scraping_enabled: errors.append("scraping_enabled is true")
    if context.html_parse_enabled: errors.append("html_parse_enabled is true")
    if context.paid_api_enabled: errors.append("paid_api_enabled is true")
    if context.dashboard_enabled: errors.append("dashboard_enabled is true")
    if context.network_default_enabled: errors.append("network_default_enabled is true")
    if context.network_used: errors.append("network_used is true")
    if context.paid_api_used: errors.append("paid_api_used is true")
    if context.scraping_used: errors.append("scraping_used is true")
    if context.html_parsing_used: errors.append("html_parsing_used is true")
    if context.broker_used: errors.append("broker_used is true")
    if context.order_created: errors.append("order_created is true")
    if context.paper_state_mutated: errors.append("paper_state_mutated is true")
    if context.telegram_real_sent: errors.append("telegram_real_sent is true")
    if context.dashboard_started: errors.append("dashboard_started is true")
    if context.produces_trade_signal: errors.append("produces_trade_signal is true")
    if context.produces_order_decision: errors.append("produces_order_decision is true")
    if context.produces_portfolio_weights: errors.append("produces_portfolio_weights is true")
    return errors

def validate_feature_enrichment_results_safety(results: list[FeatureEnrichmentResult]) -> list[str]:
    errors = []
    for r in results:
        if r.produced_trade_signal: errors.append("produced_trade_signal is true")
        if r.produced_order_decision: errors.append("produced_order_decision is true")
        if r.produced_portfolio_weights: errors.append("produced_portfolio_weights is true")
    return errors

def validate_enriched_feature_table_safety(table: EnrichedFeatureTableResult) -> list[str]:
    errors = []
    if table.produced_trade_signal: errors.append("produced_trade_signal is true")
    if table.produced_order_decision: errors.append("produced_order_decision is true")
    if table.produced_portfolio_weights: errors.append("produced_portfolio_weights is true")
    return errors

def validate_enriched_feature_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    errors = []
    for col in df.columns:
        col_lower = col.lower()
        if "signal" in col_lower and col_lower != "macd_signal_9":
            errors.append(f"Forbidden column: {col}")
            continue
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in col_lower:
                errors.append(f"Forbidden column: {col}")
                break
    return errors

def enriched_feature_output_text_has_trade_or_execution_language(text: str) -> bool:
    text_lower = text.lower()
    phrases = [
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "canlıya alındı", "kesin al", "kesin sat", "garanti kâr",
        "buy signal", "sell signal", "strong buy", "strong sell"
    ]
    for p in phrases:
        if p in text_lower:
            return True
    return False

def collect_feature_enrichment_risk_flags(context: FeatureEnrichmentContext | None = None) -> list[FeatureEnrichmentRiskFlag]:
    flags = []
    if context:
        errors = validate_feature_enrichment_context_safety(context)
        if errors:
            flags.append(FeatureEnrichmentRiskFlag.ENRICHMENT_SCHEMA_INVALID)
    return flags

def enriched_feature_output_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def enriched_feature_output_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safe output"
    return "\n".join(errors)
