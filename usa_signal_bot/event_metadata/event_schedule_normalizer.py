
import datetime
from typing import List, Dict, Any
from usa_signal_bot.core.enums import MarketEventKind, MarketEventTimingStatus, MarketEventImportance, MarketEventSource
from usa_signal_bot.event_metadata.phase111_models import UnifiedMarketEvent, create_unified_event_id

def normalize_to_unified_event(payload: Dict[str, Any]) -> UnifiedMarketEvent:
    return UnifiedMarketEvent(
        unified_event_id=create_unified_event_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        event_kind=MarketEventKind.UNKNOWN,
        source=MarketEventSource.LOCAL_FIXTURE,
        symbol=payload.get("symbol"),
        country=payload.get("country"),
        event_name=payload.get("event_name", "Unknown Event"),
        scheduled_at_utc=payload.get("scheduled_at_utc"),
        timing_status=MarketEventTimingStatus.UNKNOWN_TIME,
        importance=MarketEventImportance.UNKNOWN,
        metadata_only=True,
        source_ref_id=None,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def normalize_many_to_unified_events(payloads: List[Dict[str, Any]]) -> List[UnifiedMarketEvent]:
    return [normalize_to_unified_event(p) for p in payloads]

def validate_unified_market_event(event: UnifiedMarketEvent) -> List[str]:
    errs = []
    if not event.metadata_only: errs.append("Not metadata_only")
    return errs

def unified_event_summary(events: List[UnifiedMarketEvent]) -> Dict[str, Any]:
    return {"count": len(events)}

def unified_event_to_text(event: UnifiedMarketEvent) -> str:
    return f"Event: {event.event_name}"
