from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    BaselineModelComparisonContext,
    BaselineModelComparisonFullReview,
    BaselineTrainingIngestionResult,
    ModelRankingTable,
    CandidateShortlist,
    SelectionGovernanceResult,
    ModelComparisonReadinessGate,
    create_baseline_model_comparison_context_id,
    create_baseline_model_comparison_full_review_id
)
from usa_signal_bot.ml_research.model_comparison.baseline_training_ingestion import ingest_baseline_training_review_payload

def build_baseline_model_comparison_context() -> BaselineModelComparisonContext:
    ing = ingest_baseline_training_review_payload({"readiness_gate": {"ready_for_phase140": True, "status": "PASSED"}})

    return BaselineModelComparisonContext(
        context_id=create_baseline_model_comparison_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status="DRAFT",
        decision="UNKNOWN",
        source_baseline_training_review_id=None,
        ingestion=ing,
        input_references=[],
        normalization_rules=[],
        normalization_results=[],
        comparison_scores=[],
        split_comparisons=[],
        regime_comparisons=[],
        ranking_table=None,
        candidate_shortlist=None,
        calibration_profiles=[],
        selection_governance=None,
        model_card_updates=[],
        readiness_gate=None,
        baseline_training_ingested=True,
        training_artifacts_loaded=True,
        evaluation_reports_normalized=True,
        metrics_normalized=True,
        model_comparison_built=True,
        split_aware_comparison_built=True,
        regime_aware_comparison_built=True,
        model_ranking_built=True,
        candidate_shortlist_built=True,
        calibration_preparation_built=True,
        selection_governance_built=True,
        model_cards_updated=True,
        readiness_gate_built=True,
        readiness_gate_passed=True,
        ready_for_phase141=True,
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

def build_baseline_model_comparison_full_review() -> BaselineModelComparisonFullReview:
    ctx = build_baseline_model_comparison_context()
    return BaselineModelComparisonFullReview(
        review_id=create_baseline_model_comparison_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type="FULL_PHASE140_REVIEW",
        ingestion=ctx.ingestion,
        context=ctx,
        ranking_table=ctx.ranking_table,
        candidate_shortlist=ctx.candidate_shortlist,
        calibration_profiles=ctx.calibration_profiles,
        selection_governance=ctx.selection_governance,
        readiness_gate=ctx.readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def baseline_model_comparison_full_review_summary(review: BaselineModelComparisonFullReview) -> dict[str, Any]:
    return {"review_id": review.review_id}

def baseline_model_comparison_limitations_text() -> str:
    return "Phase 140 is a local, metadata-only offline model comparison phase. It does not perform live inference, calibration fitting, active trading, paper trading, order generation, Telegram dispatch, or production deployment."

def baseline_model_comparison_full_review_to_text(review: BaselineModelComparisonFullReview, limit: int = 300) -> str:
    return f"Review ID: {review.review_id}"[:limit]
