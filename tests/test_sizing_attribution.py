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

def test_sizing_blocked_or_reduced_summary_edge_cases():
    # Setup
    events = [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", sizing_status="BLOCKED", net_pnl_usd=0.0, gross_pnl_usd=0.0, total_cost_usd=0.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", sizing_status="CAPPED", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", sizing_status="SUPPRESSED", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e4", symbol="AMZN", sizing_status="THROTTLED", net_pnl_usd=20.0, gross_pnl_usd=25.0, total_cost_usd=5.0),
        AttributionTradeEvent(event_id="e5", symbol="META", sizing_status="UNKNOWN", net_pnl_usd=10.0, gross_pnl_usd=15.0, total_cost_usd=5.0),
    ]

    # Execution
    summary = sizing_blocked_or_reduced_summary(events)

    # Verification
    assert "BLOCKED" in summary
    assert summary["BLOCKED"]["count"] == 1
    assert summary["BLOCKED"]["net_pnl"] == 0.0

    assert "CAPPED" in summary
    assert summary["CAPPED"]["count"] == 1
    assert summary["CAPPED"]["net_pnl"] == 100.0

    assert "SUPPRESSED" in summary
    assert summary["SUPPRESSED"]["count"] == 1
    assert summary["SUPPRESSED"]["net_pnl"] == -50.0

    assert "THROTTLED" in summary
    assert summary["THROTTLED"]["count"] == 1
    assert summary["THROTTLED"]["net_pnl"] == 20.0

    assert "UNKNOWN" not in summary

def test_sizing_blocked_or_reduced_summary_empty():
    assert sizing_blocked_or_reduced_summary([]) == {}
