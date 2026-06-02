import pytest
from usa_signal_bot.backtesting.execution_latency_assumptions import build_default_execution_latency_assumption

def test_execution_latency():
    l = build_default_execution_latency_assumption()
    assert l.assumption_valid is True
