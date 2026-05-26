import pandas as pd
from typing import Any
from usa_signal_bot.core.enums import FeatureEnrichmentQuality
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureEnrichmentResult,
    EnrichedFeatureTableResult
)
from usa_signal_bot.feature_engine.enriched_features.interaction_schema_validator import validate_interaction_column_names

def validate_feature_enrichment_result(result: FeatureEnrichmentResult) -> list[str]:
    errors = []
    if result.produced_trade_signal:
        errors.append("produced_trade_signal is true")
    if result.produced_order_decision:
        errors.append("produced_order_decision is true")
    if result.produced_portfolio_weights:
        errors.append("produced_portfolio_weights is true")
    return errors

def validate_enriched_feature_table_result(result: EnrichedFeatureTableResult) -> list[str]:
    errors = []
    if result.produced_trade_signal:
        errors.append("produced_trade_signal is true")
    if result.produced_order_decision:
        errors.append("produced_order_decision is true")
    if result.produced_portfolio_weights:
        errors.append("produced_portfolio_weights is true")
    return errors

def validate_enriched_feature_dataframe(df: pd.DataFrame) -> list[str]:
    return validate_interaction_column_names(list(df.columns))

def validate_no_forbidden_enriched_feature_columns(columns: list[str]) -> list[str]:
    return validate_interaction_column_names(columns)

def feature_enrichment_quality_from_errors(errors: list[str], warnings: list[str] | None = None) -> FeatureEnrichmentQuality:
    if errors:
        return FeatureEnrichmentQuality.INVALID
    if warnings:
        return FeatureEnrichmentQuality.WARNING
    return FeatureEnrichmentQuality.HIGH

def enriched_feature_computation_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def enriched_feature_computation_validator_to_text(errors: list[str]) -> str:
    if not errors:
        return "Valid computation"
    return "\n".join(errors)
