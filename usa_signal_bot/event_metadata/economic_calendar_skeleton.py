
import datetime
from pathlib import Path
from typing import List, Dict, Any
from usa_signal_bot.core.enums import MarketEventKind, MarketEventImportance, MarketEventSource, MarketEventTimingStatus
from usa_signal_bot.event_metadata.phase111_models import EconomicEventMetadata, UnifiedMarketEvent, create_event_id, create_unified_event_id

def build_sample_economic_events() -> List[EconomicEventMetadata]:
    return [
        EconomicEventMetadata(
            event_id=create_event_id("eco"),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            event_name="Nonfarm Payrolls",
            event_kind=MarketEventKind.ECONOMIC_RELEASE,
            scheduled_at_utc=None,
            country="US",
            currency="USD",
            importance=MarketEventImportance.HIGH,
            source=MarketEventSource.LOCAL_FIXTURE,
            actual_value=None,
            forecast_value=None,
            previous_value=None,
            unit="K",
            metadata_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def load_economic_events_fixture(path: Path) -> List[EconomicEventMetadata]:
    return build_sample_economic_events()

def normalize_economic_event_payload(payload: Dict[str, Any]) -> EconomicEventMetadata:
    return build_sample_economic_events()[0]

def validate_economic_events(events: List[EconomicEventMetadata]) -> List[str]:
    errs = []
    for e in events:
        if not e.metadata_only: errs.append("Not metadata_only")
    return errs

def economic_calendar_to_unified_events(events: List[EconomicEventMetadata]) -> List[UnifiedMarketEvent]:
    u = []
    for e in events:
        u.append(UnifiedMarketEvent(
            unified_event_id=create_unified_event_id(),
            created_at_utc=e.created_at_utc,
            event_kind=e.event_kind,
            source=e.source,
            symbol=None,
            country=e.country,
            event_name=e.event_name,
            scheduled_at_utc=e.scheduled_at_utc,
            timing_status=MarketEventTimingStatus.UNKNOWN_TIME,
            importance=e.importance,
            metadata_only=e.metadata_only,
            source_ref_id=e.event_id,
            warnings=e.warnings,
            errors=e.errors,
            risk_flags=e.risk_flags,
            metadata=e.metadata
        ))
    return u

def economic_calendar_to_text(events: List[EconomicEventMetadata], limit: int = 200) -> str:
    return f"Economic Calendar: {len(events)} events"
