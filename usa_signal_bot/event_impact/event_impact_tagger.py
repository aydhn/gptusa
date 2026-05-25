
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import EventImpactCategory, EventImpactConfidence, EventImpactDirection
from usa_signal_bot.event_impact.phase112_models import EventImpactTag, create_event_impact_tag_id, _now

def infer_impact_category(event_kind: str, event_name: Optional[str] = None, importance: Optional[str] = None) -> EventImpactCategory:
    k = str(event_kind).upper()
    n = str(event_name).upper() if event_name else ""
    i = str(importance).upper() if importance else ""

    if "FOMC" in n or "FED" in n or "CPI" in n or "NFP" in n or "GDP" in n or "VIX" in n or i == "HIGH":
        return EventImpactCategory.MACRO_HIGH_IMPACT
    if k == "MACRO":
        return EventImpactCategory.MACRO_MEDIUM_IMPACT
    if k == "EARNINGS":
        return EventImpactCategory.EARNINGS_HIGH_IMPACT
    if k == "CORPORATE_ACTION" or k == "DIVIDEND" or k == "SPLIT":
        return EventImpactCategory.CORPORATE_ACTION_HIGH_IMPACT
    if k == "NEWS":
        return EventImpactCategory.NEWS_METADATA_INFORMATIONAL
    if k == "HOLIDAY":
        return EventImpactCategory.MARKET_HOLIDAY_CONTEXT
    return EventImpactCategory.LOW_IMPACT_CONTEXT

def infer_impact_confidence(event_payload: Dict[str, Any]) -> EventImpactConfidence:
    return EventImpactConfidence.MEDIUM

def compute_event_importance_score(event_payload: Dict[str, Any]) -> float:
    return 50.0

def compute_event_timing_score(event_payload: Dict[str, Any]) -> float:
    return 50.0

def compute_event_context_score(event_payload: Dict[str, Any]) -> float:
    return 50.0

def tag_event_impact(event_payload: Dict[str, Any]) -> EventImpactTag:
    cat = infer_impact_category(event_payload.get("kind", ""), event_payload.get("name"), event_payload.get("importance"))

    return EventImpactTag(
        impact_tag_id=create_event_impact_tag_id(),
        created_at_utc=_now(),
        source_event_id=event_payload.get("event_id"),
        symbol=event_payload.get("symbol"),
        event_name=event_payload.get("name", "Unknown Event"),
        event_kind=event_payload.get("kind", "UNKNOWN"),
        impact_category=cat,
        impact_direction=EventImpactDirection.UNKNOWN_CONTEXT,
        impact_confidence=infer_impact_confidence(event_payload),
        importance_score=compute_event_importance_score(event_payload),
        timing_score=compute_event_timing_score(event_payload),
        context_score=compute_event_context_score(event_payload),
        research_context_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        explanation="Tagged for research context only."
    )

def tag_many_event_impacts(events: List[Dict[str, Any]]) -> List[EventImpactTag]:
    return [tag_event_impact(e) for e in events]

def event_impact_tagger_summary(tags: List[EventImpactTag]) -> Dict[str, Any]:
    return {"total_tags": len(tags)}

def event_impact_tagger_to_text(tags: List[EventImpactTag], limit: int = 200) -> str:
    return f"Tagged {len(tags)} events."
