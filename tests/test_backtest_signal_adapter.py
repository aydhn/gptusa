import pytest
from usa_signal_bot.core.enums import SignalAction, BacktestSignalMode, BacktestOrderSide
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.signal_adapter import (
    default_signal_to_order_config, validate_signal_to_order_config,
    should_signal_create_order, signal_to_order_intent
)

def test_default_config_valid():
    config = default_signal_to_order_config()
    validate_signal_to_order_config(config)

def test_should_signal_create_order():
    config = default_signal_to_order_config()
    config.min_score = 50.0
    s1 = StrategySignal("id1", "s1", "AAPL", "1d", "2023-01-01T00:00:00Z", SignalAction.LONG, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 100.0, [], {}, [])
    s2 = StrategySignal("id2", "s1", "AAPL", "1d", "2023-01-01T00:00:00Z", SignalAction.LONG, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 40.0, [], {}, [])

    assert should_signal_create_order(s1, config)[0] == True
    assert should_signal_create_order(s2, config)[0] == False

def test_watch_mode_creates_long():
    config = default_signal_to_order_config()
    s1 = StrategySignal("id1", "s1", "AAPL", "1d", "2023-01-01T00:00:00Z", SignalAction.WATCH, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 100.0, [], {}, [])
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="2023", open=100.0, high=105.0, low=95.0, close=100.0, volume=1000)
    intent = signal_to_order_intent(s1, bar, config)
    assert intent.side == BacktestOrderSide.BUY
