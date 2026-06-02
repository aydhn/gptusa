import pytest
from usa_signal_bot.backtesting.backtest_foundation_report import build_backtest_foundation_context

def test_backtest_readiness_gate():
    ctx = build_backtest_foundation_context()
    # ingestion is missing/invalid in dummy context, so readiness should fail
    assert ctx.readiness_gate.ready_for_phase147 is False
