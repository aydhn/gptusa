
import datetime
from typing import List, Dict, Any
from usa_signal_bot.core.enums import MarketEventKind
from usa_signal_bot.event_metadata.phase111_models import EventScheduleIndex, EventSchedule, UnifiedMarketEvent, create_event_schedule_index_id

def build_event_schedule_index(schedule: EventSchedule) -> EventScheduleIndex:
    by_symbol = {}
    by_date = {}
    by_kind = {}
    by_importance = {}
    for e in schedule.events:
        if e.symbol:
            by_symbol.setdefault(e.symbol, []).append(e.unified_event_id)
        if e.scheduled_at_utc:
            date_str = e.scheduled_at_utc[:10]
            by_date.setdefault(date_str, []).append(e.unified_event_id)
        by_kind.setdefault(e.event_kind.value, []).append(e.unified_event_id)
        by_importance.setdefault(e.importance.value, []).append(e.unified_event_id)

    return EventScheduleIndex(
        index_id=create_event_schedule_index_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        schedule_id=schedule.schedule_id,
        by_symbol=by_symbol,
        by_date=by_date,
        by_kind=by_kind,
        by_importance=by_importance,
        total_indexed_events=len(schedule.events),
        index_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def events_for_symbol(symbol: str, schedule: EventSchedule) -> List[UnifiedMarketEvent]:
    return [e for e in schedule.events if e.symbol == symbol]

def events_for_date(date_str: str, schedule: EventSchedule) -> List[UnifiedMarketEvent]:
    return [e for e in schedule.events if e.scheduled_at_utc and e.scheduled_at_utc.startswith(date_str)]

def events_by_kind(kind: MarketEventKind, schedule: EventSchedule) -> List[UnifiedMarketEvent]:
    return [e for e in schedule.events if e.event_kind == kind]

def validate_event_schedule_index(index: EventScheduleIndex) -> List[str]:
    return []

def event_schedule_index_to_text(index: EventScheduleIndex, limit: int = 200) -> str:
    return f"Index for schedule {index.schedule_id}"
