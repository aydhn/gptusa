"""Phase 139 Reporting Helpers"""
from typing import Any
from .phase139_models import (
    BaselineScaffoldingIngestionResult, BaselineTrainingJobSpec, BaselineFittedModelArtifact,
    OfflinePredictionArtifact, OfflineEvaluationMetricResult, OfflineEvaluationReport,
    NonActivationModelRegistryEntry, NonActivationModelRegistry, BaselineModelCardUpdate,
    BaselineTrainingBoundaryResult, BaselineTrainingReadinessGate, BaselineTrainingContext,
    BaselineTrainingFullReview
)

def baseline_scaffolding_ingestion_result_to_text(item: BaselineScaffoldingIngestionResult) -> str:
    return "Ingestion report"

def baseline_training_job_to_text(item: BaselineTrainingJobSpec) -> str:
    return "Job spec"

def fitted_model_artifact_to_text(item: BaselineFittedModelArtifact) -> str:
    return "Artifact"

def offline_prediction_artifact_to_text(item: OfflinePredictionArtifact) -> str:
    return "Prediction"

def offline_evaluation_metric_result_to_text(item: OfflineEvaluationMetricResult) -> str:
    return "Metric"

def offline_evaluation_report_to_text(item: OfflineEvaluationReport, limit: int = 300) -> str:
    return "Evaluation report"

def non_activation_model_registry_entry_to_text(item: NonActivationModelRegistryEntry) -> str:
    return "Registry entry"

def non_activation_model_registry_to_text(item: NonActivationModelRegistry, limit: int = 300) -> str:
    return "Registry"

def baseline_model_card_update_to_text(item: BaselineModelCardUpdate, limit: int = 300) -> str:
    return "Card update"

def baseline_training_boundary_to_text(item: BaselineTrainingBoundaryResult, limit: int = 300) -> str:
    return "Boundary"

def baseline_training_readiness_gate_to_text(item: BaselineTrainingReadinessGate, limit: int = 300) -> str:
    return "Gate"

def baseline_training_context_to_text(item: BaselineTrainingContext, limit: int = 300) -> str:
    return "Context"

def baseline_training_full_review_to_text(item: BaselineTrainingFullReview, limit: int = 300) -> str:
    return "Full review"

def baseline_training_store_summary_to_text(summary: dict[str, Any]) -> str:
    return "Store summary"

def baseline_training_limitations_text() -> str:
    return "Limitations"
