
import pytest
from usa_signal_bot.event_impact.phase112_models import (
    EventImpactTag, EventImpactDirection, EventImpactCategory, EventImpactConfidence, create_event_impact_tag_id, _now
)
from usa_signal_bot.event_impact.event_impact_tagger import tag_event_impact
from usa_signal_bot.event_impact.event_impact_safety_validator import validate_impact_tags_safety

def test_event_impact_tagger():
    payload = {"event_id": "e1", "symbol": "AAPL", "name": "Q1 Earnings", "kind": "EARNINGS"}
    tag = tag_event_impact(payload)
    assert tag.impact_category == EventImpactCategory.EARNINGS_HIGH_IMPACT
    assert not tag.produces_trade_signal
    assert not tag.produces_order_decision

def test_safety_validator():
    tag = EventImpactTag(
        impact_tag_id=create_event_impact_tag_id(),
        created_at_utc=_now(),
        source_event_id="e1",
        symbol="AAPL",
        event_name="Bad Event",
        event_kind="UNKNOWN",
        impact_category=EventImpactCategory.UNKNOWN,
        impact_direction=EventImpactDirection.UNKNOWN_CONTEXT,
        impact_confidence=EventImpactConfidence.UNKNOWN,
        importance_score=50,
        timing_score=50,
        context_score=50,
        research_context_only=True,
        produces_trade_signal=True, # UNSAFE
        produces_order_decision=False,
        explanation="Buy signal!" # UNSAFE
    )

    errs = validate_impact_tags_safety([tag])
    assert len(errs) == 2
