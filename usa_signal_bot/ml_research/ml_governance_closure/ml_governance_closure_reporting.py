from typing import Any

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    DriftMonitoringIngestionResult,
    ExplainabilityInputReference,
    FeatureAttributionProxy,
    FactorContributionSummary,
    ModelBehaviorExplanation,
    RegimeAwareExplanation,
    CalibrationAwareExplanation,
    EnsembleExplanation,
    ExplainabilityReport,
    MLGovernanceClosureResult,
    AdvancedMLArtifactLineage,
    AdvancedMLFinalAuditResult,
    NonActivationMLClosureBoundaryResult,
    FinalMLModelCardClosure,
    AdvancedMLAcceptanceGate,
    AdvancedMLClosureContext,
    AdvancedMLClosureFullReview
)

def drift_monitoring_ingestion_result_to_text(item: DriftMonitoringIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id} - Valid for Phase 145: {item.valid_for_phase145}"

def explainability_input_reference_to_text(item: ExplainabilityInputReference) -> str:
    return f"Input Reference {item.input_ref_id} ({item.input_kind.value})"

def feature_attribution_proxy_to_text(item: FeatureAttributionProxy) -> str:
    return f"Feature {item.feature_name} (Rank: {item.rank})"

def factor_contribution_summary_to_text(item: FactorContributionSummary) -> str:
    return f"Factor {item.factor_name} (Rank: {item.contribution_rank})"

def model_behavior_explanation_to_text(item: ModelBehaviorExplanation, limit: int = 300) -> str:
    return f"Behavior Explanation {item.explanation_id}"

def regime_aware_explanation_to_text(item: RegimeAwareExplanation, limit: int = 300) -> str:
    return f"Regime Explanation {item.explanation_id} ({item.regime_label})"

def calibration_aware_explanation_to_text(item: CalibrationAwareExplanation, limit: int = 300) -> str:
    return f"Calibration Explanation {item.explanation_id}"

def ensemble_explanation_to_text(item: EnsembleExplanation, limit: int = 300) -> str:
    return f"Ensemble Explanation {item.explanation_id}"

def explainability_report_to_text(item: ExplainabilityReport, limit: int = 300) -> str:
    return f"Explainability Report {item.report_id} - Valid: {item.report_valid}"

def ml_governance_closure_to_text(item: MLGovernanceClosureResult, limit: int = 300) -> str:
    return f"Governance Closure {item.closure_id} - Passed: {item.closure_passed}"

def artifact_lineage_to_text(item: AdvancedMLArtifactLineage, limit: int = 300) -> str:
    return f"Artifact Lineage {item.lineage_id} - Complete: {item.lineage_complete}"

def advanced_ml_final_audit_to_text(item: AdvancedMLFinalAuditResult, limit: int = 300) -> str:
    return f"Final Audit {item.audit_id} - Passed: {item.audit_passed}"

def non_activation_ml_closure_boundary_to_text(item: NonActivationMLClosureBoundaryResult, limit: int = 300) -> str:
    return f"Non-Activation Boundary {item.boundary_id} - Passed: {item.boundary_passed}"

def final_ml_model_card_closure_to_text(item: FinalMLModelCardClosure, limit: int = 300) -> str:
    return f"Model Card Closure {item.closure_id}"

def advanced_ml_acceptance_gate_to_text(item: AdvancedMLAcceptanceGate, limit: int = 300) -> str:
    return f"Acceptance Gate {item.gate_id} - Passed: {item.status.value}"

def advanced_ml_closure_context_to_text(item: AdvancedMLClosureContext, limit: int = 300) -> str:
    return f"Closure Context {item.context_id} - Ready for Phase 146: {item.ready_for_phase146}"

def advanced_ml_closure_full_review_to_text(item: AdvancedMLClosureFullReview, limit: int = 300) -> str:
    return f"Full Review {item.review_id} - Ready for Phase 146: {item.context.ready_for_phase146}"

def ml_governance_closure_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Dir: {summary['store_dir']} (Reviews: {summary['review_count']})"

def advanced_ml_closure_limitations_text() -> str:
    return (
        "Phase 145 is an offline research and metadata-only band.\n"
        "It DOES NOT produce trade signals, trigger active trading, deploy models, or enable live inference."
    )
