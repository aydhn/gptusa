
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from usa_signal_bot.core.enums import EventImpactRiskFlag
from usa_signal_bot.event_impact.phase112_models import (
    EventMetadataIngestionResult,
    create_event_metadata_ingestion_id,
    _now
)

def event_metadata_supports_phase112(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if not payload:
        return False, ["Payload is empty"]

    if payload.get("produces_trade_signal", False) or payload.get("produces_order_decision", False):
        return False, ["Payload produces trade signal or order decision"]

    for key in ["network_used", "paid_api_used", "scraping_used", "html_parsing_used",
                "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "dashboard_started"]:
        if payload.get(key, False):
            return False, [f"Payload indicates {key}"]

    if not payload.get("metadata_only", False) or not payload.get("research_context_only", False):
        return False, ["Payload is not metadata_only and research_context_only"]

    return True, warnings

def extract_event_metadata_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context", payload) if payload else None

def extract_event_schedule(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = extract_event_metadata_context(payload)
    if not ctx: return None
    return ctx.get("schedule", ctx.get("event_schedule", {}))

def extract_unified_events(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    ctx = extract_event_metadata_context(payload)
    if not ctx: return []
    return ctx.get("unified_events", [])

def ingest_event_metadata_review_payload(payload: Dict[str, Any]) -> EventMetadataIngestionResult:
    valid, errs = event_metadata_supports_phase112(payload)

    return EventMetadataIngestionResult(
        ingestion_id=create_event_metadata_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context_id") if "context_id" in payload else None,
        available=bool(payload),
        event_metadata_ready=payload.get("event_metadata_ready", False) if payload else False,
        macro_metadata_ready=payload.get("macro_metadata_ready", False) if payload else False,
        calendar_metadata_ready=payload.get("calendar_metadata_ready", False) if payload else False,
        news_metadata_ready=payload.get("news_metadata_ready", False) if payload else False,
        event_schedule_ready=bool(extract_event_schedule(payload)),
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
        valid_for_phase112=valid,
        warnings=errs,
        errors=errs if not valid else []
    )

def ingest_latest_event_metadata_review_from_store(data_root: Path) -> EventMetadataIngestionResult:
    import json
    import logging
    try:
        from usa_signal_bot.event_metadata.event_metadata_store import get_latest_event_metadata_review
        path = get_latest_event_metadata_review(data_root)
        if path and path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                res = ingest_event_metadata_review_payload(data)
                res.source_path = str(path)
                return res
    except Exception as e:
        logging.error(f"Failed to ingest from store: {e}")
        pass

    return EventMetadataIngestionResult(
        ingestion_id=create_event_metadata_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=False,
        event_metadata_ready=False,
        macro_metadata_ready=False,
        calendar_metadata_ready=False,
        news_metadata_ready=False,
        event_schedule_ready=False,
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
        valid_for_phase112=False,
        errors=["Could not find or load event metadata review from store."]
    )

def event_metadata_ingestion_to_text(result: EventMetadataIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Valid: {result.valid_for_phase112}"
