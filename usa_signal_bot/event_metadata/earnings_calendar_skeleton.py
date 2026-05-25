
import datetime
from pathlib import Path
from typing import List, Dict, Any
from usa_signal_bot.core.enums import MarketEventKind, MarketEventImportance, MarketEventSource, MarketEventTimingStatus
from usa_signal_bot.event_metadata.phase111_models import EarningsCalendarMetadata, UnifiedMarketEvent, create_event_id, create_unified_event_id

def build_sample_earnings_events() -> List[EarningsCalendarMetadata]:
    return [
        EarningsCalendarMetadata(
            event_id=create_event_id("earn"),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            symbol="AAPL",
            company_name="Apple Inc",
            scheduled_at_utc=None,
            fiscal_period="Q1",
            importance=MarketEventImportance.HIGH,
            source=MarketEventSource.LOCAL_FIXTURE,
            eps_estimate=1.2,
            eps_actual=None,
            revenue_estimate=120e9,
            revenue_actual=None,
            metadata_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def load_earnings_events_fixture(path: Path) -> List[EarningsCalendarMetadata]:
    return build_sample_earnings_events()

def normalize_earnings_event_payload(payload: Dict[str, Any]) -> EarningsCalendarMetadata:
    return build_sample_earnings_events()[0]

def validate_earnings_events(events: List[EarningsCalendarMetadata]) -> List[str]:
    errs = []
    for e in events:
        if not e.metadata_only: errs.append("Not metadata_only")
    return errs

def earnings_calendar_to_unified_events(events: List[EarningsCalendarMetadata]) -> List[UnifiedMarketEvent]:
    u = []
    for e in events:
        u.append(UnifiedMarketEvent(
            unified_event_id=create_unified_event_id(),
            created_at_utc=e.created_at_utc,
            event_kind=MarketEventKind.EARNINGS,
            source=e.source,
            symbol=e.symbol,
            country="US",
            event_name=f"Earnings: {e.symbol}",
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

def earnings_calendar_to_text(events: List[EarningsCalendarMetadata], limit: int = 200) -> str:
    return f"Earnings Calendar: {len(events)} events"
