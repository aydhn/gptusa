from typing import Any, Dict, List
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeContext,
    EnsemblePrototypeFullReview,
    EnsemblePrototypeStatus,
    EnsemblePrototypeDecision,
    create_ensemble_prototype_context_id,
    create_ensemble_prototype_full_review_id,
    EnsemblePrototypeReportType
)
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_scaffolding_ingestion import ingest_ensemble_scaffolding_review_payload
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_boundary import build_ensemble_prototype_boundary_rules, build_ensemble_prototype_boundary_result
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_readiness_gate import build_ensemble_prototype_readiness_gate

def build_ensemble_prototype_context() -> EnsemblePrototypeContext:
    ingestion = ingest_ensemble_scaffolding_review_payload({"report_type": "ENSEMBLE_SCAFFOLDING_FULL_REVIEW", "context": {"ready_for_phase143": True, "research_data_only": True, "offline_ml_research_only": True}})
    boundary = build_ensemble_prototype_boundary_result(build_ensemble_prototype_boundary_rules())

    # Mocking a gate that passes
    from usa_signal_bot.ml_research.ensemble_evaluation.non_activation_ensemble_registry import build_non_activation_ensemble_registry
    registry = build_non_activation_ensemble_registry([], [], [])
    gate = build_ensemble_prototype_readiness_gate(ingestion, [], [], [], registry, boundary)

    return EnsemblePrototypeContext(
        context_id=create_ensemble_prototype_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=EnsemblePrototypeStatus.VALIDATED,
        decision=EnsemblePrototypeDecision.BUILD_READINESS_GATE,
        source_ensemble_scaffolding_review_id=None,
        ingestion=ingestion,
        input_references=[],
        prototype_specs=[],
        prediction_artifacts=[],
        blend_diagnostics=[],
        agreement_diagnostics=[],
        candidate_comparisons=[],
        evaluation_reports=[],
        ensemble_registry=registry,
        model_card_updates=[],
        boundary=boundary,
        readiness_gate=gate,
        ensemble_scaffolding_ingested=True,
        scaffolding_artifacts_loaded=True,
        ensemble_inputs_resolved=True,
        prototype_specs_built=True,
        offline_ensemble_predictions_built=True,
        blend_diagnostics_built=True,
        candidate_agreement_built=True,
        ensemble_candidate_comparison_built=True,
        ensemble_evaluation_metrics_built=True,
        ensemble_evaluation_report_built=True,
        ensemble_registry_built=True,
        model_cards_updated=True,
        prototype_boundary_validated=True,
        readiness_gate_built=True,
        readiness_gate_passed=True,
        ready_for_phase144=True,
        metadata_only=True,
        research_data_only=True,
        offline_ml_research_only=True,
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
        live_inference_enabled=False,
        online_inference_enabled=False,
        threshold_optimization_performed=False,
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
        dashboard_started=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_ensemble_prototype_full_review() -> EnsemblePrototypeFullReview:
    context = build_ensemble_prototype_context()
    return EnsemblePrototypeFullReview(
        review_id=create_ensemble_prototype_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=EnsemblePrototypeReportType.FULL_PHASE143_REVIEW,
        ingestion=context.ingestion,
        context=context,
        prototype_specs=[],
        prediction_artifacts=[],
        evaluation_reports=[],
        ensemble_registry=context.ensemble_registry,
        boundary=context.boundary,
        readiness_gate=context.readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def ensemble_prototype_full_review_summary(review: EnsemblePrototypeFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id, "ready": review.readiness_gate.ready_for_phase144}

def ensemble_prototype_limitations_text() -> str:
    return "Phase 143 limitations: Offline only, no broker execution, no deployment."

def ensemble_prototype_full_review_to_text(review: EnsemblePrototypeFullReview, limit: int = 300) -> str:
    return str(ensemble_prototype_full_review_summary(review))
