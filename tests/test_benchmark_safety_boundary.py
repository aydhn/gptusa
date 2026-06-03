import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_safety_boundary import (
    build_benchmark_safety_boundary_rules,
    build_benchmark_safety_boundary_result
)

def test_safety_boundary():
    ctx = {"live_trading_enabled": False}
    rules = build_benchmark_safety_boundary_rules(ctx)
    res = build_benchmark_safety_boundary_result(rules)
    assert res.boundary_passed is True

    ctx_bad = {"live_trading_enabled": True}
    rules_bad = build_benchmark_safety_boundary_rules(ctx_bad)
    res_bad = build_benchmark_safety_boundary_result(rules_bad)
    assert res_bad.boundary_passed is False
