import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent, AttributionScorecard
from usa_signal_bot.core.enums import AttributionQuality
from usa_signal_bot.attribution.attribution_scorecard import (
    calculate_attribution_quality_score, calculate_cost_efficiency_score, build_attribution_scorecard
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
    ]

def test_calculate_attribution_quality_score():
    events = _get_mock_events()
    assert calculate_attribution_quality_score(events) == 100.0

    events.append(AttributionTradeEvent(event_id="e3", symbol="GOOG")) # no pnl
    assert round(calculate_attribution_quality_score(events), 1) == 66.7

def test_calculate_cost_efficiency_score():
    events = _get_mock_events()
    # Gross: 110 + (-40) = 70. Cost: 20. Efficiency: 100 - (20/70)*100 = 100 - 28.57 = 71.4
    assert round(calculate_cost_efficiency_score(events), 1) == 71.4

def test_build_attribution_scorecard():
    events = _get_mock_events()
    scorecard = build_attribution_scorecard(events)
    assert scorecard.total_trade_count == 2
    assert scorecard.total_net_pnl_usd == 50.0
    assert scorecard.total_cost_usd == 20.0
    assert scorecard.attribution_quality in [AttributionQuality.WEAK, AttributionQuality.NOISY, AttributionQuality.INSUFFICIENT_DATA, AttributionQuality.ACCEPTABLE]
