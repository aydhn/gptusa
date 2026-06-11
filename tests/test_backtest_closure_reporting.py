import pytest
from usa_signal_bot.backtesting.closure.backtest_closure_reporting import (
    backtest_closure_limitations_text,
)


def test_backtest_closure_limitations_text():
    text = backtest_closure_limitations_text()
    assert isinstance(text, str)
    assert "Phase 152 is a read-only final audit" in text
