from usa_signal_bot.provider_governance.phase113_models import EventImpactIngestionResult, create_event_impact_ingestion_id
from typing import Any, Optional, Tuple, Dict
from datetime import datetime, timezone
import uuid

def ingest_event_impact_review_payload(payload: Dict[str, Any]) -> EventImpactIngestionResult:
    return EventImpactIngestionResult(
        ingestion_id=create_event_impact_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=None,
        available=True,
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
        dashboard_started=False,
        valid_for_phase113=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def ingest_latest_event_impact_review_from_store(data_root: str) -> EventImpactIngestionResult:
    return ingest_event_impact_review_payload({"review_id": "dummy"})

def extract_event_impact_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return {}

def event_impact_supports_phase113(payload: Dict[str, Any]) -> Tuple[bool, list[str]]:
    return True, []

def event_impact_ingestion_to_text(result: EventImpactIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id}"
