import pytest
from usa_signal_bot.core.enums import BacktestEventType
from usa_signal_bot.core.exceptions import BacktestEventError
from usa_signal_bot.backtesting.event_models import (
    create_backtest_event, sort_events_by_time_sequence, filter_events_by_type,
    event_to_dict, validate_backtest_event
)

def test_create_backtest_event():
    event = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-01T00:00:00Z", "AAPL", "1d", {"price": 100}, 1)
    assert event.event_type == BacktestEventType.MARKET_BAR
    assert event.symbol == "AAPL"
    assert event.sequence == 1

def test_validate_invalid_sequence():
    event = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-01T00:00:00Z", "AAPL", "1d", {"price": 100}, -1)
    with pytest.raises(BacktestEventError):
        validate_backtest_event(event)

def test_sort_events():
    e1 = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-02T00:00:00Z", "AAPL", "1d", {}, 1)
    e2 = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-01T00:00:00Z", "AAPL", "1d", {}, 1)
    e3 = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-01T00:00:00Z", "AAPL", "1d", {}, 0)

    sorted_events = sort_events_by_time_sequence([e1, e2, e3])
    assert sorted_events[0] == e3
    assert sorted_events[1] == e2
    assert sorted_events[2] == e1

def test_filter_events():
    e1 = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-02T00:00:00Z", "AAPL", "1d", {}, 1)
    e2 = create_backtest_event(BacktestEventType.SIGNAL, "2023-01-01T00:00:00Z", "AAPL", "1d", {}, 1)
    filtered = filter_events_by_type([e1, e2], BacktestEventType.SIGNAL)
    assert len(filtered) == 1
    assert filtered[0].event_type == BacktestEventType.SIGNAL

def test_event_to_dict():
    event = create_backtest_event(BacktestEventType.MARKET_BAR, "2023-01-01T00:00:00Z", "AAPL", "1d", {"price": 100}, 1)
    d = event_to_dict(event)
    assert d["event_type"] == "MARKET_BAR"
    assert d["symbol"] == "AAPL"
