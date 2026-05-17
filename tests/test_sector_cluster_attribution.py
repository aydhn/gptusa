import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.sector_cluster_attribution import (
    sector_performance_attribution, cluster_performance_attribution, sector_cluster_cost_drag_summary
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", sector="Tech", cluster="Growth", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="XOM", sector="Energy", cluster="Value", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
    ]

def test_sector_attribution():
    events = _get_mock_events()
    contribs = sector_performance_attribution(events)
    assert len(contribs) == 2
    assert contribs[0].name == "Tech"

def test_cluster_attribution():
    events = _get_mock_events()
    contribs = cluster_performance_attribution(events)
    assert len(contribs) == 2
    assert contribs[0].name == "Growth"

def test_cost_drag_summary():
    events = _get_mock_events()
    summary = sector_cluster_cost_drag_summary(events)
    assert "Tech" in summary["sectors"]
    assert "Growth" in summary["clusters"]
