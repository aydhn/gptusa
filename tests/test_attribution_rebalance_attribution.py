import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.rebalance_attribution import turnover_cost_attribution

def test_turnover_cost_attribution_empty():
    assert turnover_cost_attribution([]) == []

def test_turnover_cost_attribution_sorting():
    event1 = AttributionTradeEvent(
        event_id="e1", symbol="AAPL", rebalance_action_type="INCREASE", total_cost_usd=10.0, net_pnl_usd=50.0
    )
    event2 = AttributionTradeEvent(
        event_id="e2", symbol="MSFT", rebalance_action_type="DECREASE", total_cost_usd=25.0, net_pnl_usd=30.0
    )
    event3 = AttributionTradeEvent(
        event_id="e3", symbol="GOOG", rebalance_action_type="INCREASE", total_cost_usd=5.0, net_pnl_usd=20.0
    )
    event4 = AttributionTradeEvent(
        event_id="e4", symbol="AMZN", rebalance_action_type="NEW", total_cost_usd=8.0, net_pnl_usd=10.0
    )

    events = [event1, event2, event3, event4]
    contribs = turnover_cost_attribution(events)

    assert len(contribs) == 3
    assert contribs[0].name == "DECREASE"
    assert contribs[0].total_cost_usd == 25.0
    assert contribs[1].name == "INCREASE"
    assert contribs[1].total_cost_usd == 15.0
    assert contribs[2].name == "NEW"
    assert contribs[2].total_cost_usd == 8.0

def test_turnover_cost_attribution_with_none_costs():
    event1 = AttributionTradeEvent(
        event_id="e1", symbol="AAPL", rebalance_action_type="INCREASE", total_cost_usd=None, net_pnl_usd=50.0
    )
    event2 = AttributionTradeEvent(
        event_id="e2", symbol="MSFT", rebalance_action_type="DECREASE", total_cost_usd=None, net_pnl_usd=30.0
    )
    event3 = AttributionTradeEvent(
        event_id="e3", symbol="GOOG", rebalance_action_type="INCREASE", total_cost_usd=5.0, net_pnl_usd=20.0
    )

    events = [event1, event2, event3]
    contribs = turnover_cost_attribution(events)

    assert len(contribs) == 2
    assert contribs[0].name == "INCREASE"
    assert contribs[0].total_cost_usd == 5.0
    assert contribs[1].name == "DECREASE"
    assert contribs[1].total_cost_usd == 0.0
