import pytest
from usa_signal_bot.backtesting.backtest_foundation_reporting import backtest_foundation_limitations_text

def test_reporting():
    txt = backtest_foundation_limitations_text()
    assert "Phase 146" in txt
