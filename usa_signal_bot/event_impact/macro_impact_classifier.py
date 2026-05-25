
from typing import Any, Dict, List
from usa_signal_bot.core.enums import EventImpactDirection
from usa_signal_bot.event_impact.phase112_models import EventImpactTag
from usa_signal_bot.event_impact.event_impact_tagger import tag_event_impact

def macro_event_direction_context(event_payload: Dict[str, Any]) -> EventImpactDirection:
    return EventImpactDirection.NEUTRAL_CONTEXT

def macro_event_direction_context_notes(event_payload: Dict[str, Any]) -> str:
    return "Neutral macro_event_direction context."

def classify_macro_event_impact(event_payload: Dict[str, Any]) -> EventImpactTag:
    tag = tag_event_impact(event_payload)
    tag.impact_direction = macro_event_direction_context(event_payload)
    tag.explanation = macro_event_direction_context_notes(event_payload)
    return tag

def macro_impact_classifier_summary(tags: List[EventImpactTag]) -> Dict[str, Any]:
    return {"total": len(tags)}

def macro_impact_classifier_to_text(tag: EventImpactTag) -> str:
    return tag.explanation
