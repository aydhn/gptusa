from typing import Dict, Any, List
from usa_signal_bot.core.enums import BaselineMLScaffoldingStatus, BaselineMLScaffoldingDecision, BaselineMLScaffoldingReportType
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineMLScaffoldingContext,
    BaselineMLScaffoldingFullReview,
    MLDatasetAssemblyIngestionResult,
    BaselineExperimentRegistry,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    NonActivationEvaluationBoundaryResult,
    BaselineExperimentReadinessGate,
    create_baseline_ml_scaffolding_context_id,
    create_baseline_ml_scaffolding_full_review_id,
    _now_utc
)

def build_baseline_ml_scaffolding_context(
    ingestion: MLDatasetAssemblyIngestionResult,
    registry: BaselineExperimentRegistry,
    harness: EvaluationHarnessContract,
    boundary: PredictionOutputBoundary,
    non_activation: NonActivationEvaluationBoundaryResult,
    readiness: BaselineExperimentReadinessGate
) -> BaselineMLScaffoldingContext:

    return BaselineMLScaffoldingContext(
        context_id=create_baseline_ml_scaffolding_context_id(),
        created_at_utc=_now_utc(),
        status=BaselineMLScaffoldingStatus.VALIDATED if readiness.ready_for_phase139 else BaselineMLScaffoldingStatus.BLOCKED,
        decision=BaselineMLScaffoldingDecision.BUILD_READINESS_GATE,
        source_dataset_assembly_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        model_family_specs=registry.model_family_specs,
        experiment_specs=registry.experiment_specs,
        metric_specs=registry.metric_specs,
        evaluation_harness_contract=harness,
        prediction_output_boundary=boundary,
        model_card_drafts=registry.model_card_drafts,
        experiment_registry=registry,
        non_activation_boundary=non_activation,
        readiness_gate=readiness,
        dataset_assembly_ingested=True,
        dataset_artifacts_loaded=True,
        experiment_specs_built=True,
        model_family_registry_built=True,
        metric_specs_built=True,
        evaluation_harness_contract_built=True,
        prediction_output_boundary_built=True,
        model_card_draft_built=True,
        experiment_registry_built=True,
        non_activation_boundary_validated=True,
        readiness_gate_built=True,
        readiness_gate_passed=readiness.ready_for_phase139,
        ready_for_phase139=readiness.ready_for_phase139,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        daemon_started=False,
        scheduler_enabled=False,
        training_started=False,
        prediction_started=False,
        model_training_used=False,
        model_prediction_used=False,
        heavy_ml_dependency_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False
    )

def build_baseline_ml_scaffolding_full_review(context: BaselineMLScaffoldingContext) -> BaselineMLScaffoldingFullReview:
    return BaselineMLScaffoldingFullReview(
        review_id=create_baseline_ml_scaffolding_full_review_id(),
        created_at_utc=_now_utc(),
        report_type=BaselineMLScaffoldingReportType.FULL_PHASE138_REVIEW,
        ingestion=context.ingestion,
        context=context,
        experiment_registry=context.experiment_registry,
        evaluation_harness_contract=context.evaluation_harness_contract,
        prediction_output_boundary=context.prediction_output_boundary,
        non_activation_boundary=context.non_activation_boundary,
        readiness_gate=context.readiness_gate,
        output_paths={}
    )

def baseline_ml_scaffolding_limitations_text() -> str:
    return "Phase 138 is a scaffolding phase. It does not train models or execute predictions. It explicitly forbids active trading, broker execution, paper state mutation, Telegram sends, deployment, and live-daemon execution."

def baseline_ml_scaffolding_full_review_summary(review: BaselineMLScaffoldingFullReview) -> Dict[str, Any]:
    return {
        "ready_for_phase139": review.readiness_gate.ready_for_phase139,
        "experiments": review.experiment_registry.experiment_count,
        "harness_valid": review.evaluation_harness_contract.contract_valid,
        "non_activation_passed": review.non_activation_boundary.boundary_passed
    }

def baseline_ml_scaffolding_full_review_to_text(review: BaselineMLScaffoldingFullReview, limit: int = 300) -> str:
    summary = baseline_ml_scaffolding_full_review_summary(review)
    return f"Phase 138 Full Review: Ready={summary['ready_for_phase139']}, Experiments={summary['experiments']}, Non-Activation={summary['non_activation_passed']}"
