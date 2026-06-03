import pytest
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import StrategyBenchmarkAlignment, StrategyBenchmarkAlignedPoint, BenchmarkKind
from usa_signal_bot.backtesting.benchmark_comparison.relative_performance_metrics import calculate_relative_performance_metrics

def test_calculate_metrics():
    pts = [
        StrategyBenchmarkAlignedPoint(point_id="1", created_at_utc="", run_id="r1", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, timestamp="t1", strategy_equity=100.0, strategy_return=0.0, strategy_cumulative_return=0.0, benchmark_equity=100.0, benchmark_return=0.0, benchmark_cumulative_return=0.0, tracking_difference=0.0),
        StrategyBenchmarkAlignedPoint(point_id="2", created_at_utc="", run_id="r1", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, timestamp="t2", strategy_equity=102.0, strategy_return=0.02, strategy_cumulative_return=0.02, benchmark_equity=101.0, benchmark_return=0.01, benchmark_cumulative_return=0.01, tracking_difference=0.01)
    ]
    alg = StrategyBenchmarkAlignment(alignment_id="a1", created_at_utc="", run_id="r1", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, aligned_points=pts, alignment_valid=True)

    metrics = calculate_relative_performance_metrics("r1", alg)
    assert len(metrics) > 0
    excess = next(m for m in metrics if m.metric_name == "Excess Total Return")
    assert excess.value == pytest.approx(0.01)
