from typing import Any
from usa_signal_bot.core.enums import FactorCompositionReportType, FactorCompositionStatus, FactorCompositionDecision
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FactorCompositionContext,
    FactorCompositionFullReview,
    create_factor_composition_context_id,
    create_factor_composition_full_review_id,
    _now_str
)

def build_factor_composition_context() -> FactorCompositionContext:
    # A skeleton context builder, this would normally take in the outputs from all prior builders
    # This acts as an aggregator of the subcomponents
    return FactorCompositionContext(
        context_id=create_factor_composition_context_id(),
        created_at_utc=_now_str(),
        status=FactorCompositionStatus.DRAFT,
        decision=FactorCompositionDecision.UNKNOWN,
        source_feature_enrichment_review_id=None,
        ingestion=None,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
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
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
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

def build_factor_composition_full_review(context: FactorCompositionContext) -> FactorCompositionFullReview:
    return FactorCompositionFullReview(
        review_id=create_factor_composition_full_review_id(),
        created_at_utc=_now_str(),
        report_type=FactorCompositionReportType.FULL_PHASE120_REVIEW,
        ingestion=context.ingestion,
        context=context,
        feature_groups=context.feature_groups,
        group_profiles=context.group_profiles,
        factor_candidates=context.factor_candidates,
        composition_spec=context.composition_spec,
        selection_metadata=context.selection_metadata,
        readiness_gate=context.readiness_gate,
        output_paths={}
    )

def factor_composition_full_review_summary(review: FactorCompositionFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "report_type": review.report_type.value,
        "context_status": review.context.status.value,
        "feature_groups_ready": review.context.feature_groups_ready,
        "factor_candidates_ready": review.context.factor_candidates_ready,
        "selection_metadata_ready": review.context.selection_metadata_ready,
        "ready_for_phase121": review.context.ready_for_phase121
    }

def factor_composition_limitations_text() -> str:
    return """Phase 120 Factor Composition Limitations:
- This phase is not strategy activation.
- This phase is not a signal engine.
- Broker APIs, paper orders, and paper state mutation are strictly disabled.
- Telegram real send, web scraping, HTML parsing, and Dashboards are not allowed.
- Paid APIs and Network calls are forbidden.
- Factor candidates do NOT represent investment advice or trade recommendations.
- Factor computations occur locally and only on artifacts pre-computed offline.
- Portfolio construction weights are not computed in this phase.
"""

def factor_composition_full_review_to_text(review: FactorCompositionFullReview, limit: int = 300) -> str:
    summary = factor_composition_full_review_summary(review)
    lines = [
        f"Factor Composition Full Review: {summary['review_id']}",
        f"Status: {summary['context_status']}",
        f"Ready for Phase 121: {summary['ready_for_phase121']}",
        f"Limitations:\n{factor_composition_limitations_text()}"
    ]
    return "\n".join(lines)
