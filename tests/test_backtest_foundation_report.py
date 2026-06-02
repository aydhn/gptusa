import pytest
from usa_signal_bot.backtesting.backtest_foundation_report import build_backtest_foundation_full_review

def test_build_review():
    r = build_backtest_foundation_full_review()
    assert r.report_type.value == "FULL_PHASE146_REVIEW"
