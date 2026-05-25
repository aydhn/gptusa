
import datetime
from typing import List, Dict, Any
from usa_signal_bot.core.enums import EventScheduleStatus
from usa_signal_bot.event_metadata.phase111_models import EventSchedule, UnifiedMarketEvent, create_event_schedule_id

def build_event_schedule(events: List[UnifiedMarketEvent]) -> EventSchedule:
    return EventSchedule(
        schedule_id=create_event_schedule_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=EventScheduleStatus.CREATED,
        events=events,
        total_events=len(events),
        macro_event_count=0,
        earnings_event_count=0,
        corporate_action_count=0,
        news_metadata_count=0,
        duplicate_count=0,
        invalid_time_count=0,
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
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_event_schedule() -> EventSchedule:
    return build_event_schedule([])

def validate_event_schedule_safety(schedule: EventSchedule) -> List[str]:
    errs = []
    if not schedule.metadata_only: errs.append("Not metadata_only")
    if not schedule.research_context_only: errs.append("Not research_context_only")
    if schedule.produces_trade_signal: errs.append("Produces trade signal")
    if schedule.produces_order_decision: errs.append("Produces order decision")
    if schedule.network_used: errs.append("Network used")
    if schedule.broker_used: errs.append("Broker used")
    if schedule.paper_state_mutated: errs.append("Paper state mutated")
    return errs

def event_schedule_summary(schedule: EventSchedule) -> Dict[str, Any]:
    return {"total": schedule.total_events}

def event_schedule_to_text(schedule: EventSchedule, limit: int = 300) -> str:
    return f"Event Schedule: {schedule.total_events} events"
