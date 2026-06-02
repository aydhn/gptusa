import pytest
from usa_signal_bot.backtesting.execution_assumptions import build_default_execution_assumption

def test_execution_assumption():
    a = build_default_execution_assumption()
    assert a.allow_live_execution is False
