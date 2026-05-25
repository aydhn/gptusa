
import datetime
from typing import Dict, Any, List
from usa_signal_bot.core.enums import EventMetadataStatus, EventMetadataDecision, EventMetadataReportType
from usa_signal_bot.event_metadata.phase111_models import (
    EventMetadataContext, EventMetadataFullReview,
    create_event_metadata_context_id, create_event_metadata_full_review_id
)
from usa_signal_bot.event_metadata.provider_orchestration_ingestion import ingest_latest_provider_orchestration_review_from_store
from usa_signal_bot.event_metadata.macro_metadata_catalog import build_default_macro_series_catalog
from usa_signal_bot.event_metadata.economic_calendar_skeleton import build_sample_economic_events
from usa_signal_bot.event_metadata.earnings_calendar_skeleton import build_sample_earnings_events
from usa_signal_bot.event_metadata.corporate_actions_skeleton import build_sample_corporate_actions
from usa_signal_bot.event_metadata.news_metadata_skeleton import build_sample_news_metadata
from usa_signal_bot.event_metadata.event_schedule_builder import build_default_event_schedule
from usa_signal_bot.event_metadata.event_schedule_index import build_event_schedule_index

def build_event_metadata_context() -> EventMetadataContext:
    ingest = ingest_latest_provider_orchestration_review_from_store(None)
    macro = build_default_macro_series_catalog()
    eco = build_sample_economic_events()
    earn = build_sample_earnings_events()
    corp = build_sample_corporate_actions()
    news = build_sample_news_metadata()
    sched = build_default_event_schedule()
    idx = build_event_schedule_index(sched)

    return EventMetadataContext(
        context_id=create_event_metadata_context_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=EventMetadataStatus.CREATED,
        decision=EventMetadataDecision.INCONCLUSIVE,
        source_provider_orchestration_review_id=ingest.source_review_id,
        ingestion=ingest,
        macro_series=macro,
        economic_events=eco,
        earnings_events=earn,
        corporate_actions=corp,
        news_metadata=news,
        schedule=sched,
        schedule_index=idx,
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
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_event_metadata_full_review() -> EventMetadataFullReview:
    ctx = build_event_metadata_context()
    return EventMetadataFullReview(
        review_id=create_event_metadata_full_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_type=EventMetadataReportType.FULL_PHASE111_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        schedule=ctx.schedule,
        schedule_index=ctx.schedule_index,
        macro_series=ctx.macro_series,
        economic_events=ctx.economic_events,
        earnings_events=ctx.earnings_events,
        corporate_actions=ctx.corporate_actions,
        news_metadata=ctx.news_metadata,
        output_paths={},
        warnings=[],
        errors=[]
    )

def event_metadata_full_review_summary(review: EventMetadataFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def event_metadata_limitations_text() -> str:
    return "Phase 111 is metadata skeleton. No broker, no paper mutation, no network."

def event_metadata_full_review_to_text(review: EventMetadataFullReview, limit: int = 300) -> str:
    return f"Review: {review.review_id}\n" + event_metadata_limitations_text()
