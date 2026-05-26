from typing import Any
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureFactorKickoffIngestionResult, IndicatorDefinition, FeatureDefinition,
    FactorDefinition, FeatureInputContract, FeatureOutputSchema,
    FeatureComputationRequest, FeatureComputationResult, FeatureRegistry,
    FeatureFoundationContext, FeatureFoundationFullReview
)

def feature_factor_kickoff_ingestion_result_to_text(item: FeatureFactorKickoffIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id} - Ready: {item.ready_for_phase116}"

def indicator_definition_to_text(item: IndicatorDefinition) -> str:
    return f"Indicator {item.name} [{item.category.value}]"

def feature_definition_to_text(item: FeatureDefinition) -> str:
    return f"Feature {item.name} [{item.category.value}]"

def factor_definition_to_text(item: FactorDefinition) -> str:
    return f"Factor {item.name} [{item.category.value}]"

def feature_input_contract_to_text(item: FeatureInputContract) -> str:
    return f"Contract {item.contract_id} - Valid: {item.contract_valid}"

def feature_output_schema_to_text(item: FeatureOutputSchema, limit: int = 200) -> str:
    return f"Schema {item.schema_id} - Valid: {item.schema_valid}"

def feature_computation_request_to_text(item: FeatureComputationRequest) -> str:
    return f"Request {item.request_id} for {item.symbol}"

def feature_computation_result_to_text(item: FeatureComputationResult) -> str:
    return f"Result {item.result_id} - Passed: {item.passed}"

def feature_registry_to_text(item: FeatureRegistry, limit: int = 300) -> str:
    return f"Registry {item.registry_id} - Features: {item.total_features}, Indicators: {item.total_indicators}, Factors: {item.total_factors}"

def feature_foundation_context_to_text(item: FeatureFoundationContext, limit: int = 300) -> str:
    return f"Context {item.context_id} - Status: {item.status.value}"

def feature_foundation_full_review_to_text(item: FeatureFoundationFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id} - Phase 117 Ready: {item.context.ready_for_phase117}"

def feature_foundation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Contexts: {summary.get('contexts', 0)}, Reviews: {summary.get('reviews', 0)}"

def feature_foundation_limitations_text() -> str:
    return "Limitations: No trade signal, no activation, no broker, no order, no telegram, no dashboard."
