
from typing import Any, Dict, List
from usa_signal_bot.core.enums import EventImpactDirection
from usa_signal_bot.event_impact.phase112_models import EventImpactTag
from usa_signal_bot.event_impact.event_impact_tagger import tag_event_impact

def earnings_surprise_context(event_payload: Dict[str, Any]) -> EventImpactDirection:
    return EventImpactDirection.NEUTRAL_CONTEXT

def earnings_event_context_notes(event_payload: Dict[str, Any]) -> str:
    return "Neutral earnings_surprise context."

def classify_earnings_event_impact(event_payload: Dict[str, Any]) -> EventImpactTag:
    tag = tag_event_impact(event_payload)
    tag.impact_direction = earnings_surprise_context(event_payload)
    tag.explanation = earnings_event_context_notes(event_payload)
    return tag

def earnings_impact_classifier_summary(tags: List[EventImpactTag]) -> Dict[str, Any]:
    return {"total": len(tags)}
