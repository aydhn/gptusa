from typing import Any, Dict, List
from .phase142_models import (
    EnsembleScaffoldingContext,
    EnsembleScaffoldingFullReview,
    EnsembleScaffoldingReportType,
    EnsembleScaffoldingStatus,
    EnsembleScaffoldingDecision,
    create_ensemble_scaffolding_context_id,
    create_ensemble_scaffolding_full_review_id,
    _now
)
from .calibration_diagnostics_ingestion import ingest_calibration_diagnostics_review_payload
from .ensemble_governance import build_ensemble_governance_result
from .non_activation_ensemble_boundary import build_non_activation_ensemble_boundary_result
from .ensemble_readiness_gate import build_ensemble_readiness_gate

def build_ensemble_scaffolding_context() -> EnsembleScaffoldingContext:
    # Dummy mock
    ing = ingest_calibration_diagnostics_review_payload({})
    gov = build_ensemble_governance_result([], [], [])
    bound = build_non_activation_ensemble_boundary_result([])
    gate = build_ensemble_readiness_gate(ing, [], gov, bound)

    return EnsembleScaffoldingContext(
        context_id=create_ensemble_scaffolding_context_id(),
        created_at_utc=_now(),
        status=EnsembleScaffoldingStatus.DRAFT,
        decision=EnsembleScaffoldingDecision.UNKNOWN,
        source_calibration_diagnostics_review_id=None,
        ingestion=ing,
        candidates=[],
        family_specs=[],
        candidate_groups=[],
        blend_policies=[],
        blend_plans=[],
        correlation_diagnostics=[],
        diversity_profiles=[],
        complementarity_profiles=[],
        eligibility_profiles=[],
        preparation_reports=[],
        ensemble_governance=gov,
        non_activation_boundary=bound,
        model_card_updates=[],
        readiness_gate=gate,
        calibration_diagnostics_ingested=False,
        calibration_artifacts_loaded=False,
        ensemble_candidates_resolved=False,
        ensemble_family_specs_built=False,
        candidate_groups_built=False,
        blend_policy_built=False,
        blend_coefficient_plan_built=False,
        prediction_correlation_built=False,
        diversity_profiles_built=False,
        complementarity_profiles_built=False,
        calibration_aware_eligibility_built=False,
        ensemble_preparation_report_built=False,
        ensemble_governance_built=False,
        non_activation_boundary_validated=False,
        model_cards_updated=False,
        readiness_gate_built=False,
        readiness_gate_passed=False,
        ready_for_phase143=False,
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


        calibration_fitting_performed=False,
        calibrated_model_created=False,
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

def build_ensemble_scaffolding_full_review() -> EnsembleScaffoldingFullReview:
    ctx = build_ensemble_scaffolding_context()
    return EnsembleScaffoldingFullReview(
        review_id=create_ensemble_scaffolding_full_review_id(),
        created_at_utc=_now(),
        report_type=EnsembleScaffoldingReportType.FULL_PHASE142_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        preparation_reports=[],
        ensemble_governance=ctx.ensemble_governance,
        non_activation_boundary=ctx.non_activation_boundary,
        readiness_gate=ctx.readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def ensemble_scaffolding_full_review_summary(review: EnsembleScaffoldingFullReview) -> Dict[str, Any]:
    return {"ready": review.readiness_gate.ready_for_phase143}

def ensemble_scaffolding_limitations_text() -> str:
    return "Phase 142 is non-activation ensemble scaffolding only. No trade signals."

def ensemble_scaffolding_full_review_to_text(review: EnsembleScaffoldingFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} - Ready for Phase 143: {review.readiness_gate.ready_for_phase143}"
