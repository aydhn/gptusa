from typing import Any
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeFeatureEngineeringIngestionResult,
    RegimeLabelingSpec,
    RegimeLabelingRule,
    HeuristicRegimeLabelResult,
    RollingRegimeWindowSpec,
    RollingRegimeWindowResult,
    RegimeLabelSequence,
    RegimeLabelStabilityProfile,
    RegimeCandidateValidationResult,
    RegimeLabelingReadinessGate,
    RegimeLabelingContext,
    RegimeLabelingFullReview
)

def regime_feature_engineering_ingestion_result_to_text(item: RegimeFeatureEngineeringIngestionResult) -> str:
    from usa_signal_bot.regime_classification.labeling.regime_feature_engineering_ingestion import regime_feature_engineering_ingestion_to_text
    return regime_feature_engineering_ingestion_to_text(item)

def regime_labeling_spec_to_text(item: RegimeLabelingSpec) -> str:
    return f"Spec: {item.spec_name} ({item.method.value})"

def regime_labeling_rule_to_text(item: RegimeLabelingRule) -> str:
    return f"Rule: {item.rule_name} -> {item.label_name}"

def heuristic_regime_label_result_to_text(item: HeuristicRegimeLabelResult) -> str:
    return f"Result [{item.symbol} {item.timestamp}]: {item.assigned_label} (Conf: {item.confidence_score:.2f})"

def rolling_regime_window_spec_to_text(item: RollingRegimeWindowSpec) -> str:
    return f"Window Spec: {item.window_name} (Size: {item.window_size})"

def rolling_regime_window_result_to_text(item: RollingRegimeWindowResult) -> str:
    return f"Window Result [{item.symbol}]: {item.window_name} - Dom: {item.dominant_label} ({item.stability_score:.2f} stability)"

def regime_label_sequence_to_text(item: RegimeLabelSequence) -> str:
    return f"Sequence [{item.symbol}]: Dom: {item.dominant_label} ({item.dominant_label_ratio:.2%})"

def regime_label_stability_profile_to_text(item: RegimeLabelStabilityProfile) -> str:
    return f"Stability Profile [{item.symbol}]: Score {item.stability_score:.2f}, Quality: {item.quality.value}"

def regime_candidate_validation_result_to_text(item: RegimeCandidateValidationResult, limit: int = 300) -> str:
    from usa_signal_bot.regime_classification.labeling.candidate_validation_runner import candidate_validation_runner_to_text
    return candidate_validation_runner_to_text(item, limit)

def regime_labeling_readiness_gate_to_text(item: RegimeLabelingReadinessGate, limit: int = 300) -> str:
    from usa_signal_bot.regime_classification.labeling.regime_labeling_readiness_gate import regime_labeling_readiness_gate_to_text
    return regime_labeling_readiness_gate_to_text(item, limit)

def regime_labeling_context_to_text(item: RegimeLabelingContext, limit: int = 300) -> str:
    return f"Context: {item.context_id}, Status: {item.status.value}, Ready: {item.ready_for_phase129}"

def regime_labeling_full_review_to_text(item: RegimeLabelingFullReview, limit: int = 300) -> str:
    from usa_signal_bot.regime_classification.labeling.regime_labeling_report import regime_labeling_full_review_to_text
    return regime_labeling_full_review_to_text(item, limit)

def regime_labeling_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews']} reviews."

def regime_labeling_limitations_text() -> str:
    from usa_signal_bot.regime_classification.labeling.regime_labeling_report import regime_labeling_limitations_text
    return regime_labeling_limitations_text()
