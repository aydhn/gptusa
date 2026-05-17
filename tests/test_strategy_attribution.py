import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.strategy_attribution import (
    strategy_performance_attribution, strategy_win_rate_summary, strategy_failure_candidates
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", strategy_name="S1", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", strategy_name="S2", net_pnl_usd=-10.0, gross_pnl_usd=10.0, total_cost_usd=20.0),
    ]

def test_strategy_performance_attribution():
    events = _get_mock_events()
    contribs = strategy_performance_attribution(events)
    assert len(contribs) == 2
    assert contribs[0].name == "S1"

def test_strategy_win_rate_summary():
    events = _get_mock_events()
    summary = strategy_win_rate_summary(events)
    assert "S1" in summary
    assert summary["S1"] == 100.0

def test_strategy_failure_candidates():
    events = _get_mock_events()
    failures = strategy_failure_candidates(events)
    assert len(failures) == 1
    assert failures[0].name == "S2" # turned winner to loser
