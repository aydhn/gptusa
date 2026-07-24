import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.drawdown_attribution import (
    calculate_running_equity, drawdown_contribution_by_dimension
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0, timestamp_utc="2023-01-01T10:00:00Z"),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0, timestamp_utc="2023-01-02T10:00:00Z"),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", net_pnl_usd=-20.0, timestamp_utc="2023-01-03T10:00:00Z"),
    ]

def test_calculate_running_equity():
    events = _get_mock_events()
    points = calculate_running_equity(events, starting_equity=100.0)
    assert len(points) == 4 # 1 initial + 3 events
    assert points[0]["equity"] == 100.0
    assert points[1]["equity"] == 200.0 # AAPL
    assert points[2]["equity"] == 150.0 # MSFT -> drawdown
    assert points[2]["drawdown"] == 50.0
    assert points[3]["equity"] == 130.0 # GOOG -> more drawdown
    assert points[3]["drawdown"] == 70.0

def test_drawdown_contribution_by_dimension():
    events = _get_mock_events()
    contribs = drawdown_contribution_by_dimension(events, AttributionDimension.SYMBOL)
    assert len(contribs) == 2 # Only negative PnL symbols MSFT and GOOG
    assert contribs[0].name == "MSFT"
    assert contribs[0].drawdown_contribution_usd == 50.0

def test_calculate_running_equity_sorting():
    events = [
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0, timestamp_utc="2023-01-02T10:00:00Z"),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", net_pnl_usd=-20.0, timestamp_utc="2023-01-03T10:00:00Z"),
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0, timestamp_utc="2023-01-01T10:00:00Z"),
    ]
    points = calculate_running_equity(events, starting_equity=100.0)
    assert len(points) == 4
    assert points[0]["equity"] == 100.0
    assert points[1]["equity"] == 200.0
    assert points[1]["event_id"] == "e1"
    assert points[2]["equity"] == 150.0
    assert points[2]["event_id"] == "e2"
    assert points[3]["equity"] == 130.0
    assert points[3]["event_id"] == "e3"

def test_calculate_running_equity_no_timestamps():
    events = [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0, timestamp_utc=None),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0, timestamp_utc=None),
    ]
    points = calculate_running_equity(events, starting_equity=100.0)
    assert len(points) == 3
    assert points[0]["equity"] == 100.0
    assert points[1]["equity"] == 200.0
    assert points[1]["event_id"] == "e1"
    assert points[2]["equity"] == 150.0
    assert points[2]["event_id"] == "e2"

def test_calculate_running_equity_empty():
    points = calculate_running_equity([])
    assert len(points) == 1
    assert points[0]["equity"] == 100000.0
    assert points[0]["peak"] == 100000.0
    assert points[0]["drawdown"] == 0.0

def test_calculate_running_equity_none_pnl():
    events = [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=None, timestamp_utc="2023-01-01T10:00:00Z"),
    ]
    points = calculate_running_equity(events, starting_equity=100.0)
    assert len(points) == 2
    assert points[1]["equity"] == 100.0
    assert points[1]["peak"] == 100.0
    assert points[1]["drawdown"] == 0.0
    assert points[1]["net_pnl_usd"] == 0.0
