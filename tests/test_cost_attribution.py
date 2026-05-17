import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.cost_attribution import (
    aggregate_cost_by_dimension, aggregate_cost_by_component,
    calculate_cost_drag_pct, identify_cost_degraded_groups
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", strategy_name="S1", net_pnl_usd=90.0, gross_pnl_usd=100.0, total_cost_usd=10.0, slippage_cost_usd=5.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", strategy_name="S2", net_pnl_usd=-10.0, gross_pnl_usd=10.0, total_cost_usd=20.0, market_impact_cost_usd=10.0),
    ]

def test_aggregate_cost_by_dimension():
    events = _get_mock_events()
    contribs = aggregate_cost_by_dimension(events, AttributionDimension.SYMBOL)
    assert len(contribs) == 2
    assert contribs[0].name == "MSFT" # Sorted by cost desc (20 > 10)
    assert contribs[0].total_cost_usd == 20.0

def test_aggregate_cost_by_component():
    events = _get_mock_events()
    contribs = aggregate_cost_by_component(events)
    names = [c.name for c in contribs]
    assert "Slippage" in names
    assert "MarketImpact" in names
    assert "FeesAndCommissions" in names

def test_calculate_cost_drag_pct():
    assert calculate_cost_drag_pct(100.0, 10.0) == 10.0
    assert calculate_cost_drag_pct(-100.0, 10.0) is None
    assert calculate_cost_drag_pct(100.0, None) is None

def test_identify_cost_degraded_groups():
    events = _get_mock_events()
    contribs = aggregate_cost_by_dimension(events, AttributionDimension.SYMBOL)
    degraded = identify_cost_degraded_groups(contribs, cost_drag_threshold_pct=50.0)
    assert len(degraded) == 1
    assert degraded[0].name == "MSFT" # Drag = 20/10 = 200%
