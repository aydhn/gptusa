import pytest
from usa_signal_bot.core.enums import SignalAction, BacktestSignalMode
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.backtesting.signal_replay import (
    filter_signals_for_replay, build_signal_events, SignalReplayData, SignalReplayRequest
)

def test_filter_signals():
    s1 = StrategySignal("id1", "s1", "AAPL", "1d", "2023-01-01T00:00:00Z", SignalAction.LONG, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 100.0, [], {}, [])
    s2 = StrategySignal("id2", "s1", "MSFT", "1d", "2023-01-02T00:00:00Z", SignalAction.LONG, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 100.0, [], {}, [])

    filtered = filter_signals_for_replay([s1, s2], ["AAPL"], None, None, None)
    assert len(filtered) == 1
    assert filtered[0].symbol == "AAPL"

def test_build_signal_events():
    req = SignalReplayRequest(symbols=["AAPL"])
    s1 = StrategySignal("id1", "s1", "AAPL", "1d", "2023-01-01T00:00:00Z", SignalAction.LONG, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 100.0, [], {}, [])
    data = SignalReplayData(req, [s1])

    events = build_signal_events(data)
    assert len(events) == 1
    assert events[0].symbol == "AAPL"
