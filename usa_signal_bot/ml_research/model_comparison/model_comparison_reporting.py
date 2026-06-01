from typing import Any

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    BaselineTrainingIngestionResult,
    ModelComparisonInputReference,
    MetricNormalizationResult,
    ModelComparisonScore,
    SplitAwareComparisonResult,
    RegimeAwareComparisonResult,
    ModelRankingTable,
    CandidateShortlist,
    CalibrationReadinessProfile,
    SelectionGovernanceResult,
    ModelCardComparisonUpdate,
    ModelComparisonReadinessGate,
    BaselineModelComparisonContext,
    BaselineModelComparisonFullReview
)

def baseline_training_ingestion_result_to_text(item: BaselineTrainingIngestionResult) -> str:
    return f"Ingestion ID: {item.ingestion_id}"

def model_comparison_input_reference_to_text(item: ModelComparisonInputReference) -> str:
    return f"Ref ID: {item.reference_id}, Name: {item.artifact_name}"

def metric_normalization_result_to_text(item: MetricNormalizationResult) -> str:
    return f"Metric: {item.metric_name}, Normalized: {item.normalized_value}"

def model_comparison_score_to_text(item: ModelComparisonScore) -> str:
    return f"Model: {item.model_name}, Score: {item.score_value}"

def split_aware_comparison_to_text(item: SplitAwareComparisonResult) -> str:
    return f"Artifact: {item.model_artifact_id}, Gap: {item.generalization_gap}"

def regime_aware_comparison_to_text(item: RegimeAwareComparisonResult) -> str:
    return f"Artifact: {item.model_artifact_id}, Consistency: {item.regime_consistency_score}"

def model_ranking_table_to_text(item: ModelRankingTable, limit: int = 300) -> str:
    from usa_signal_bot.ml_research.model_comparison.ranking_engine import ranking_to_text
    return ranking_to_text(item, limit)

def candidate_shortlist_to_text(item: CandidateShortlist, limit: int = 300) -> str:
    from usa_signal_bot.ml_research.model_comparison.candidate_shortlist_builder import candidate_shortlist_to_text as short_text
    return short_text(item, limit)

def calibration_readiness_profile_to_text(item: CalibrationReadinessProfile, limit: int = 300) -> str:
    return f"Model: {item.model_name}, Ready: {item.ready_for_phase141_calibration_review}"[:limit]

def selection_governance_to_text(item: SelectionGovernanceResult, limit: int = 300) -> str:
    from usa_signal_bot.ml_research.model_comparison.selection_governance import selection_governance_to_text as gov_text
    return gov_text(item, limit)

def model_card_comparison_update_to_text(item: ModelCardComparisonUpdate, limit: int = 300) -> str:
    from usa_signal_bot.ml_research.model_comparison.model_card_comparison_updater import model_card_comparison_update_to_text as up_text
    return up_text([item], limit)

def model_comparison_readiness_gate_to_text(item: ModelComparisonReadinessGate, limit: int = 300) -> str:
    from usa_signal_bot.ml_research.model_comparison.model_comparison_readiness_gate import model_comparison_readiness_gate_to_text as g_text
    return g_text(item, limit)

def model_comparison_context_to_text(item: BaselineModelComparisonContext, limit: int = 300) -> str:
    return f"Context ID: {item.context_id}, Status: {item.status}"[:limit]

def model_comparison_full_review_to_text(item: BaselineModelComparisonFullReview, limit: int = 300) -> str:
    return f"Review ID: {item.review_id}"[:limit]

def model_comparison_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def baseline_model_comparison_limitations_text() -> str:
    return "Phase 140 is a local, metadata-only offline model comparison phase. It does not perform live inference, calibration fitting, active trading, paper trading, order generation, Telegram dispatch, or production deployment."
