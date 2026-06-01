import json
from typing import Any, Dict

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsembleScaffoldingIngestionResult,
    EnsemblePrototypeInputReference,
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    BlendContributionDiagnostic,
    CandidateAgreementDiagnostic,
    EnsembleCandidateComparisonResult,
    OfflineEnsembleEvaluationMetricResult,
    OfflineEnsembleEvaluationReport,
    NonActivationEnsembleRegistryEntry,
    NonActivationEnsembleRegistry,
    EnsembleModelCardUpdate,
    EnsemblePrototypeBoundaryResult,
    EnsemblePrototypeReadinessGate,
    EnsemblePrototypeContext,
    EnsemblePrototypeFullReview
)
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_store import _to_dict_recursive

def _render(obj, limit=300):
    s = json.dumps(_to_dict_recursive(obj), indent=2)
    if len(s) > limit:
        return s[:limit] + "...(truncated)"
    return s

def ensemble_scaffolding_ingestion_result_to_text(item: EnsembleScaffoldingIngestionResult) -> str: return _render(item)
def ensemble_prototype_input_reference_to_text(item: EnsemblePrototypeInputReference) -> str: return _render(item)
def ensemble_prototype_spec_to_text(item: EnsemblePrototypeSpec, limit: int = 300) -> str: return _render(item, limit)
def offline_ensemble_prediction_artifact_to_text(item: OfflineEnsemblePredictionArtifact) -> str: return _render(item)
def blend_contribution_diagnostic_to_text(item: BlendContributionDiagnostic) -> str: return _render(item)
def candidate_agreement_diagnostic_to_text(item: CandidateAgreementDiagnostic) -> str: return _render(item)
def ensemble_candidate_comparison_to_text(item: EnsembleCandidateComparisonResult) -> str: return _render(item)
def offline_ensemble_evaluation_metric_result_to_text(item: OfflineEnsembleEvaluationMetricResult) -> str: return _render(item)
def offline_ensemble_evaluation_report_to_text(item: OfflineEnsembleEvaluationReport, limit: int = 300) -> str: return _render(item, limit)
def non_activation_ensemble_registry_entry_to_text(item: NonActivationEnsembleRegistryEntry) -> str: return _render(item)
def non_activation_ensemble_registry_to_text(item: NonActivationEnsembleRegistry, limit: int = 300) -> str: return _render(item, limit)
def ensemble_model_card_update_to_text(item: EnsembleModelCardUpdate, limit: int = 300) -> str: return _render(item, limit)
def ensemble_prototype_boundary_to_text(item: EnsemblePrototypeBoundaryResult, limit: int = 300) -> str: return _render(item, limit)
def ensemble_prototype_readiness_gate_to_text(item: EnsemblePrototypeReadinessGate, limit: int = 300) -> str: return _render(item, limit)
def ensemble_prototype_context_to_text(item: EnsemblePrototypeContext, limit: int = 300) -> str: return _render(item, limit)
def ensemble_prototype_full_review_to_text(item: EnsemblePrototypeFullReview, limit: int = 300) -> str: return _render(item, limit)
def ensemble_prototype_store_summary_to_text(summary: Dict[str, Any]) -> str: return str(summary)
def ensemble_prototype_limitations_text() -> str: return "Offline only."
