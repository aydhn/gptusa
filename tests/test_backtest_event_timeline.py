import pytest
from usa_signal_bot.backtesting.backtest_event_timeline import build_default_backtest_event_timeline

def test_event_timeline():
    t = build_default_backtest_event_timeline()
    assert t.prevents_lookahead_bias is True
