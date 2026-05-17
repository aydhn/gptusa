import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.sizing_attribution import (
    sizing_status_attribution, sizing_blocked_or_reduced_summary
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", sizing_status="APPROVED", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", sizing_status="REDUCED", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
    ]

def test_sizing_status_attribution():
    events = _get_mock_events()
    contribs = sizing_status_attribution(events)
    assert len(contribs) == 2
    assert contribs[0].name == "APPROVED"

def test_sizing_blocked_or_reduced_summary():
    events = _get_mock_events()
    summary = sizing_blocked_or_reduced_summary(events)
    assert "REDUCED" in summary
    assert "APPROVED" not in summary
