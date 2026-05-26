from typing import Any, Dict
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    CoreIndicatorIngestionResult,
    AdvancedFeatureSpec,
    CrossSectionalUniverse,
    CrossSectionalAlignmentResult,
    NormalizationResult,
    AdvancedFeatureComputationRequest,
    AdvancedFeatureComputationResult,
    AdvancedFeatureTableResult,
    AdvancedFeatureAudit,
    AdvancedFeatureContext,
    AdvancedFeatureFullReview
)
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_report import advanced_feature_limitations_text

def core_indicator_ingestion_result_to_text(item: CoreIndicatorIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id}: Phase118Ready={item.ready_for_phase118}, ActivationAllowed={item.activation_allowed}"

def advanced_feature_spec_to_text(item: AdvancedFeatureSpec) -> str:
    return f"Spec {item.feature_name} (Family: {item.family.value})"

def cross_sectional_universe_to_text(item: CrossSectionalUniverse) -> str:
    return f"Universe {item.universe_id} ({len(item.symbols)} symbols)"

def cross_sectional_alignment_result_to_text(item: CrossSectionalAlignmentResult) -> str:
    return f"Alignment {item.alignment_id}: {item.aligned_table_count} tables aligned"

def normalization_result_to_text(item: NormalizationResult) -> str:
    return f"Norm {item.output_column} ({item.method.value})"

def advanced_feature_computation_request_to_text(item: AdvancedFeatureComputationRequest) -> str:
    return f"Request {item.request_id} ({len(item.symbols)} symbols)"

def advanced_feature_computation_result_to_text(item: AdvancedFeatureComputationResult) -> str:
    return f"Result {item.result_id}: {len(item.computed_feature_columns)} features computed"

def advanced_feature_table_result_to_text(item: AdvancedFeatureTableResult) -> str:
    return f"Table {item.symbol}: {item.rows} rows, {len(item.advanced_feature_columns)} advanced features"

def advanced_feature_audit_to_text(item: AdvancedFeatureAudit) -> str:
    return f"Audit {item.audit_id}: LocalOnly={item.local_only}"

def advanced_feature_context_to_text(item: AdvancedFeatureContext, limit: int = 300) -> str:
    return f"Context {item.context_id}: Status={item.status.value}, Ready={item.advanced_features_ready}"

def advanced_feature_full_review_to_text(item: AdvancedFeatureFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}: {len(item.specs)} specs, {len(item.feature_tables)} tables.\n{advanced_feature_limitations_text()}"

def advanced_feature_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews']} reviews saved."
