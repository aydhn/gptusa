from typing import Dict, Any
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    MLDatasetAssemblyIngestionResult,
    BaselineModelFamilySpec,
    BaselineExperimentSpec,
    EvaluationMetricSpec,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    ModelArtifactPlaceholder,
    ModelCardDraft,
    BaselineExperimentRegistry,
    NonActivationEvaluationBoundaryResult,
    BaselineExperimentReadinessGate,
    BaselineMLScaffoldingContext,
    BaselineMLScaffoldingFullReview
)
from usa_signal_bot.ml_research.experiment_scaffolding.dataset_assembly_ingestion import dataset_assembly_ingestion_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_model_family_registry import baseline_model_family_registry_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_experiment_specs import baseline_experiment_specs_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.evaluation_metric_specs import evaluation_metric_specs_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.evaluation_harness_contract import evaluation_harness_contract_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.prediction_output_boundary import prediction_output_boundary_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.model_card_draft_builder import model_card_draft_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.experiment_registry_builder import baseline_experiment_registry_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.non_activation_evaluation_boundary import non_activation_evaluation_boundary_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_experiment_readiness_gate import baseline_experiment_readiness_gate_to_text
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_scaffolding_report import baseline_ml_scaffolding_full_review_to_text, baseline_ml_scaffolding_limitations_text

def ml_dataset_assembly_ingestion_result_to_text(item: MLDatasetAssemblyIngestionResult) -> str:
    return dataset_assembly_ingestion_to_text(item)

def baseline_model_family_spec_to_text(item: BaselineModelFamilySpec) -> str:
    return f"Model Family: {item.family_name} ({item.family_kind.value})"

def baseline_experiment_spec_to_text(item: BaselineExperimentSpec) -> str:
    return f"Experiment: {item.experiment_name} ({item.experiment_kind.value})"

def evaluation_metric_spec_to_text(item: EvaluationMetricSpec) -> str:
    return f"Metric: {item.metric_name} ({item.metric_kind.value})"

def model_artifact_placeholder_to_text(item: ModelArtifactPlaceholder) -> str:
    return f"Placeholder: {item.placeholder_name}"

def baseline_scaffolding_context_to_text(item: BaselineMLScaffoldingContext, limit: int = 300) -> str:
    return f"Scaffolding Context: ID={item.context_id}, Status={item.status.value}, Ready={item.ready_for_phase139}"

def baseline_scaffolding_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews_count']} reviews."
