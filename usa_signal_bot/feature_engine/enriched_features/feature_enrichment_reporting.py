from typing import Any
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    AdvancedFeatureIngestionResult, FeatureEnrichmentSpec, FeatureInteractionSpec,
    FeatureConfidenceProfile, FeatureFreshnessProfile, FeatureEnrichmentRequest,
    FeatureEnrichmentResult, EnrichedFeatureTableResult, FeatureEnrichmentAudit,
    FeatureEnrichmentContext, FeatureEnrichmentFullReview
)

def advanced_feature_ingestion_result_to_text(item: AdvancedFeatureIngestionResult) -> str:
    return f"Ingestion valid: {item.valid_for_phase119}"

def feature_enrichment_spec_to_text(item: FeatureEnrichmentSpec) -> str:
    return f"Spec: {item.name}"

def feature_interaction_spec_to_text(item: FeatureInteractionSpec) -> str:
    return f"Interaction: {item.name}"

def feature_confidence_profile_to_text(item: FeatureConfidenceProfile) -> str:
    return f"Confidence: {item.confidence_score}"

def feature_freshness_profile_to_text(item: FeatureFreshnessProfile) -> str:
    return f"Freshness: {item.freshness_score}"

def feature_enrichment_request_to_text(item: FeatureEnrichmentRequest) -> str:
    return f"Request: {item.request_id}"

def feature_enrichment_result_to_text(item: FeatureEnrichmentResult) -> str:
    return f"Result: {item.result_id} passed: {item.passed}"

def enriched_feature_table_result_to_text(item: EnrichedFeatureTableResult) -> str:
    return f"Table: {item.symbol} rows: {item.rows}"

def feature_enrichment_audit_to_text(item: FeatureEnrichmentAudit) -> str:
    return f"Audit no_network: {item.no_network}"

def feature_enrichment_context_to_text(item: FeatureEnrichmentContext, limit: int = 300) -> str:
    return f"Context {item.context_id}"

def feature_enrichment_full_review_to_text(item: FeatureEnrichmentFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}"

def feature_enrichment_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Reviews: {summary.get('review_count', 0)}"

def feature_enrichment_limitations_text() -> str:
    return "Phase 119 is feature enrichment, not active trading."
