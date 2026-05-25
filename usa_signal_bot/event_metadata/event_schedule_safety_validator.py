
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import EventMetadataRiskFlag
from usa_signal_bot.event_metadata.phase111_models import EventMetadataContext, EventSchedule, NewsMetadataItem

def validate_event_schedule_context_safety(context: EventMetadataContext) -> List[str]:
    errs = []
    if not context.metadata_only: errs.append("Not metadata_only")
    if context.produces_trade_signal: errs.append("Produces trade signal")
    if context.broker_used: errs.append("Broker used")
    if context.paper_state_mutated: errs.append("Paper state mutated")
    if context.telegram_real_sent: errs.append("Telegram real sent")
    return errs

def validate_event_schedule_safety(schedule: EventSchedule) -> List[str]:
    errs = []
    if not schedule.metadata_only: errs.append("Not metadata_only")
    if schedule.produces_trade_signal: errs.append("Produces trade signal")
    if schedule.broker_used: errs.append("Broker used")
    return errs

def validate_news_metadata_safety(items: List[NewsMetadataItem]) -> List[str]:
    errs = []
    for i in items:
        if i.content_fetched: errs.append("Content fetched")
        if i.network_used: errs.append("Network used")
        if i.scraping_used: errs.append("Scraping used")
        if i.html_parsing_used: errs.append("HTML parsing used")
    return errs

def collect_event_metadata_risk_flags(context: Optional[EventMetadataContext] = None) -> List[EventMetadataRiskFlag]:
    return []

def event_schedule_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def event_schedule_safety_to_text(errors: List[str]) -> str:
    if not errors: return "Schedule is safe."
    return "Schedule unsafe: " + ", ".join(errors)
