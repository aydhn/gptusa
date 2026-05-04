import pytest
from usa_signal_bot.backtesting.benchmark_models import BenchmarkEquityCurve, BenchmarkSpec
from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint
from usa_signal_bot.core.enums import BenchmarkType, RelativePerformanceBucket
from usa_signal_bot.backtesting.benchmark_comparison import (
    align_equity_curves, calculate_curve_returns, calculate_correlation_like,
    calculate_beta_like, calculate_tracking_error_like, calculate_information_ratio_like,
    compare_strategy_to_benchmark, compare_strategy_to_benchmark_set
)

def build_curve(timestamps, cash_list):
    points = []
    for ts, eq in zip(timestamps, cash_list):
        points.append(EquityCurvePoint(ts, eq, eq, 0, 0, 0, 0))
    return EquityCurve(points, cash_list[0], cash_list[-1], 0, 0)

def build_benchmark_curve(timestamps, cash_list, sym="SPY"):
    points = []
    for ts, eq in zip(timestamps, cash_list):
        points.append(EquityCurvePoint(ts, eq, eq, 0, 0, 0, 0))
    spec = BenchmarkSpec(f"{sym}_ETF", f"{sym} ETF", sym, BenchmarkType.ETF)
    return BenchmarkEquityCurve(spec, points, cash_list[0], cash_list[-1], 0)

def test_align_equity_curves():
    ts1 = ["2024-01-01", "2024-01-02", "2024-01-03"]
    ts2 = ["2024-01-02", "2024-01-03", "2024-01-04"]
    c1 = build_curve(ts1, [100, 110, 120])
    c2 = build_benchmark_curve(ts2, [100, 105, 110])

    a1, a2 = align_equity_curves(c1, c2)
    assert len(a1) == 2
    assert a1[0].timestamp_utc == "2024-01-02"
    assert a2[0].timestamp_utc == "2024-01-02"

def test_metrics_calculations():
    # Simple values
    strat_ret = [0.01, 0.02, -0.01]
    bench_ret = [0.005, 0.015, -0.005]

    corr = calculate_correlation_like(strat_ret, bench_ret)
    assert corr is not None
    assert corr > 0.9 # Should be highly correlated

    beta = calculate_beta_like(strat_ret, bench_ret)
    assert beta is not None

    te = calculate_tracking_error_like(strat_ret, bench_ret)
    assert te is not None

    ir = calculate_information_ratio_like(strat_ret, bench_ret)
    assert ir is not None

def test_compare_strategy_to_benchmark():
    ts = ["2024-01-01", "2024-01-02"]
    # Strategy goes up 20%
    c1 = build_curve(ts, [100, 120])
    # Benchmark goes up 10%
    c2 = build_benchmark_curve(ts, [100, 110])

    res = compare_strategy_to_benchmark(c1, c2)
    assert res.strategy_return_pct == 20.0
    assert res.benchmark_return_pct == 10.0
    assert res.excess_return_pct == 10.0
    assert res.relative_bucket == RelativePerformanceBucket.OUTPERFORMED

def test_compare_strategy_to_benchmark_set():
    ts = ["2024-01-01", "2024-01-02"]
    c1 = build_curve(ts, [100, 120])
    c2 = build_benchmark_curve(ts, [100, 110], "SPY")
    c3 = build_benchmark_curve(ts, [100, 130], "QQQ")

    table = compare_strategy_to_benchmark_set(c1, [c2, c3])
    assert len(table.rows) == 2

    # First row is SPY (outperformed)
    assert table.rows[0].excess_return_pct == 10.0
    # Second row is QQQ (underperformed)
    assert table.rows[1].excess_return_pct == -10.0
