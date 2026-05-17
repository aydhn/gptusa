import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.time_window_attribution import time_window_performance_attribution

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0, timestamp_utc="2023-01-05T10:00:00Z"),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0, timestamp_utc="2023-01-20T10:00:00Z"),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", net_pnl_usd=200.0, timestamp_utc="2023-02-15T10:00:00Z"),
    ]

def test_time_window_performance_attribution():
    events = _get_mock_events()
    contribs = time_window_performance_attribution(events, window="monthly")
    assert len(contribs) == 2
    assert contribs[0].name == "2023-01"
    assert contribs[0].net_pnl_usd == 50.0
    assert contribs[1].name == "2023-02"
    assert contribs[1].net_pnl_usd == 200.0
