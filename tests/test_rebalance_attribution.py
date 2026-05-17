import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.rebalance_attribution import (
    rebalance_action_attribution, turnover_cost_attribution
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", rebalance_action_type="INCREASE", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", rebalance_action_type="EXIT", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=30.0),
    ]

def test_rebalance_action_attribution():
    events = _get_mock_events()
    contribs = rebalance_action_attribution(events)
    assert len(contribs) == 2
    assert contribs[0].name == "INCREASE"

def test_turnover_cost_attribution():
    events = _get_mock_events()
    contribs = turnover_cost_attribution(events)
    assert len(contribs) == 2
    assert contribs[0].name == "EXIT" # Sorted by cost
