import pytest
from usa_signal_bot.backtesting.backtest_safety_boundary import build_backtest_safety_boundary_rules, build_backtest_safety_boundary_result

def test_safety_boundary_passed():
    rules = build_backtest_safety_boundary_rules()
    res = build_backtest_safety_boundary_result(rules)
    assert res.boundary_passed is True
    assert res.no_live_trading is True
    assert res.no_full_backtest_run_phase146 is True

def test_safety_boundary_failed():
    rules = build_backtest_safety_boundary_rules({"live_trading_enabled": True})
    res = build_backtest_safety_boundary_result(rules)
    assert res.boundary_passed is False
