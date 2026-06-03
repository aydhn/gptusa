import pytest
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkReturnSeries, StrategyBenchmarkAlignment, BenchmarkKind
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_diagnostics import build_benchmark_diagnostics

def test_build_diagnostics():
    s = BenchmarkReturnSeries(series_id="s1", created_at_utc="", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE)
    a = StrategyBenchmarkAlignment(alignment_id="a1", created_at_utc="", run_id="r1", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, coverage_ratio=1.0)

    diags = build_benchmark_diagnostics([s], [a])
    assert len(diags) == 2
