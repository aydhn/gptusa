
from typing import Any, Dict, List
from usa_signal_bot.core.enums import EventImpactStatus, EventImpactDecision, EventImpactReportType
from usa_signal_bot.event_impact.phase112_models import (
    EventImpactContext, EventImpactFullReview, EventMetadataIngestionResult,
    create_event_impact_context_id, create_event_impact_full_review_id, create_event_metadata_ingestion_id, _now
)

def build_event_impact_context() -> EventImpactContext:
    ing = EventMetadataIngestionResult(
        ingestion_id=create_event_metadata_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        event_metadata_ready=True,
        macro_metadata_ready=True,
        calendar_metadata_ready=True,
        news_metadata_ready=True,
        event_schedule_ready=True,
        metadata_only=True,
        research_context_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase112=True
    )
    return EventImpactContext(
        context_id=create_event_impact_context_id(),
        created_at_utc=_now(),
        status=EventImpactStatus.CREATED,
        decision=EventImpactDecision.TAG_EVENTS,
        source_event_metadata_review_id=None,
        ingestion=ing,
        impact_tags=[],
        symbol_exposures=[],
        macro_regimes=[],
        calendar_validation_results=[],
        event_impact_ready=True,
        macro_regime_metadata_ready=True,
        calendar_aware_validation_ready=True,
        metadata_only=True,
        research_context_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
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

def build_event_impact_full_review() -> EventImpactFullReview:
    ctx = build_event_impact_context()
    return EventImpactFullReview(
        review_id=create_event_impact_full_review_id(),
        created_at_utc=_now(),
        report_type=EventImpactReportType.FULL_PHASE112_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        impact_tags=ctx.impact_tags,
        symbol_exposures=ctx.symbol_exposures,
        macro_regimes=ctx.macro_regimes,
        calendar_validation_results=ctx.calendar_validation_results,
        output_paths={}
    )

def event_impact_full_review_summary(review: EventImpactFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def event_impact_limitations_text() -> str:
    return "LIMITATIONS: No real trading, no broker, no scraping. Metadata only."

def event_impact_full_review_to_text(review: EventImpactFullReview, limit: int = 300) -> str:
    return f"Full Review {review.review_id}
" + event_impact_limitations_text()
