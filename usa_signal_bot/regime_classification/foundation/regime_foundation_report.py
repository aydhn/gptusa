from typing import Any
from usa_signal_bot.core.enums import RegimeFoundationStatus, RegimeFoundationDecision, RegimeFoundationReportType
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    RegimeFoundationContext,
    RegimeFoundationFullReview,
    create_regime_foundation_context_id,
    create_regime_foundation_full_review_id,
    _now
)
from usa_signal_bot.regime_classification.foundation.regime_foundation_safety_validator import collect_regime_foundation_risk_flags, validate_regime_foundation_context_safety

def build_regime_foundation_context(
    ingestion: Any,
    input_bundle: Any,
    dataset_contract: Any,
    dataset_skeleton: Any,
    taxonomy: Any,
    boundary: Any
) -> RegimeFoundationContext:

    ctx = RegimeFoundationContext(
        context_id=create_regime_foundation_context_id(),
        created_at_utc=_now(),
        status=RegimeFoundationStatus.CREATED,
        decision=RegimeFoundationDecision.UNKNOWN,
        source_final_closure_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        input_bundle=input_bundle,
        dataset_contract=dataset_contract,
        dataset_skeleton=dataset_skeleton,
        taxonomy=taxonomy,
        boundary=boundary,
        final_closure_ingested=True,
        frozen_artifacts_ready=input_bundle.bundle_valid,
        input_contract_ready=True,
        market_state_dataset_contract_ready=len(dataset_contract.errors) == 0,
        regime_taxonomy_ready=len(taxonomy.errors) == 0,
        non_activation_boundary_ready=boundary.boundary_passed,
        ready_for_phase127=False,
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

    ctx.ready_for_phase127 = (
        ctx.frozen_artifacts_ready and
        ctx.market_state_dataset_contract_ready and
        ctx.regime_taxonomy_ready and
        ctx.non_activation_boundary_ready and
        ingestion.valid_for_phase126
    )

    ctx.errors.extend(validate_regime_foundation_context_safety(ctx))
    if ctx.errors:
        ctx.status = RegimeFoundationStatus.BLOCKED
        ctx.decision = RegimeFoundationDecision.BLOCK
        ctx.ready_for_phase127 = False
    elif ctx.ready_for_phase127:
        ctx.status = RegimeFoundationStatus.VALIDATED
        ctx.decision = RegimeFoundationDecision.BUILD_REGIME_FOUNDATION

    ctx.risk_flags = collect_regime_foundation_risk_flags(ctx)
    return ctx

def build_regime_foundation_full_review(context: RegimeFoundationContext) -> RegimeFoundationFullReview:
    return RegimeFoundationFullReview(
        review_id=create_regime_foundation_full_review_id(),
        created_at_utc=_now(),
        report_type=RegimeFoundationReportType.FULL_PHASE126_REVIEW,
        ingestion=context.ingestion,
        context=context,
        input_bundle=context.input_bundle,
        dataset_contract=context.dataset_contract,
        dataset_skeleton=context.dataset_skeleton,
        taxonomy=context.taxonomy,
        boundary=context.boundary,
        output_paths={},
        warnings=context.warnings,
        errors=context.errors
    )

def regime_foundation_full_review_summary(review: RegimeFoundationFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase127": review.context.ready_for_phase127,
        "error_count": len(review.errors)
    }

def regime_foundation_limitations_text() -> str:
    return """
Phase 126 Limitations:
- Phase 126 is NOT activation.
- Phase 126 is NOT a strategy/signal engine.
- Phase 126 does NOT perform regime model training.
- Phase 126 does NOT perform regime prediction.
- Phase 126 is NOT deployment.
- Phase 126 does NOT use broker APIs.
- Phase 126 does NOT create paper orders.
- Phase 126 does NOT mutate paper state.
- Phase 126 does NOT send real Telegram messages.
- Phase 126 does NOT scrape websites.
- Phase 126 does NOT parse HTML.
- Phase 126 does NOT use dashboards.
- Phase 126 does NOT use paid APIs.
- Phase 126 tests do NOT use the real network.
- Regime labels are NOT investment advice.
- Phase 126 does NOT perform portfolio construction.
"""

def regime_foundation_full_review_to_text(review: RegimeFoundationFullReview, limit: int = 300) -> str:
    lines = [
        f"Regime Foundation Review ID: {review.review_id}",
        f"Ready for Phase 127: {review.context.ready_for_phase127}",
        f"Context Status: {review.context.status.value}",
        f"Decision: {review.context.decision.value}"
    ]
    if review.errors:
        lines.append("Errors:")
        for err in review.errors:
            lines.append(f"  - {err}")
    lines.append(regime_foundation_limitations_text())
    return "\n".join(lines)
