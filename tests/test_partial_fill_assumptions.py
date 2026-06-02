import pytest
from usa_signal_bot.backtesting.partial_fill_assumptions import build_default_partial_fill_assumption

def test_partial_fill():
    a = build_default_partial_fill_assumption()
    assert a.assumption_valid is True
