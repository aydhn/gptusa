from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeAlignmentContext, RegimeAlignmentFullReview, create_regime_alignment_context_id,
    create_regime_alignment_full_review_id, RegimeAlignmentReportType, RegimeAlignmentStatus,
    RegimeAlignmentDecision, _now
)
from usa_signal_bot.regime_classification.alignment.alignment_readiness_gate import regime_alignment_readiness_passed

def build_regime_alignment_context() -> RegimeAlignmentContext:
    return RegimeAlignmentContext(
        context_id=create_regime_alignment_context_id(),
        created_at_utc=_now(),
        status=RegimeAlignmentStatus.DRAFT,
        decision=RegimeAlignmentDecision.UNKNOWN,
        source_market_behavior_review_id=None,
        metadata_only=True, research_data_only=True,
        activation_allowed=False, strategy_activation_allowed=False, deployment_allowed=False,
        active_paper_enabled=False, broker_execution_enabled=False, order_creation_enabled=False,
        paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False,
        html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False,
        network_default_enabled=False, model_training_used=False, model_prediction_used=False,
        heavy_ml_dependency_used=False, produces_trade_signal=False, produces_order_decision=False,
        produces_portfolio_weights=False, investment_advice=False, network_used=False,
        paid_api_used=False, scraping_used=False, html_parsing_used=False, broker_used=False,
        order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False
    )

def build_regime_alignment_full_review(context: RegimeAlignmentContext) -> RegimeAlignmentFullReview:
    return RegimeAlignmentFullReview(
        review_id=create_regime_alignment_full_review_id(),
        created_at_utc=_now(),
        report_type=RegimeAlignmentReportType.FULL_PHASE131_REVIEW,
        ingestion=context.ingestion,
        context=context,
        frozen_factor_refs=context.frozen_factor_refs,
        overlay_results=context.overlay_results,
        compatibility_results=context.compatibility_results,
        diagnostics_profiles=context.diagnostics_profiles,
        readiness_gate=context.readiness_gate,
        output_paths={},
        warnings=context.warnings,
        errors=context.errors
    )

def regime_alignment_full_review_summary(review: RegimeAlignmentFullReview) -> dict[str, Any]:
    return {"id": review.review_id}

def regime_alignment_limitations_text() -> str:
    return "Phase 131 is regime-aware alignment, NOT activation/deployment."

def regime_alignment_full_review_to_text(review: RegimeAlignmentFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} - Ready: {review.readiness_gate.ready_for_phase132 if review.readiness_gate else False}"
