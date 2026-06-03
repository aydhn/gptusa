import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkReturnSeries, BenchmarkCurvePoint, BenchmarkKind
from usa_signal_bot.backtesting.benchmark_comparison.strategy_benchmark_alignment import align_strategy_and_benchmark_returns

def test_align_strategy_benchmark():
    s_df = pd.DataFrame({
        "timestamp": ["2024-01-01", "2024-01-02"],
        "simulated_equity": [100.0, 102.0],
        "simple_return": [0.0, 0.02],
        "cumulative_return": [0.0, 0.02]
    })
    pts = [
        BenchmarkCurvePoint(point_id="1", created_at_utc="", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, timestamp="2024-01-01", simulated_benchmark_equity=100.0, benchmark_simple_return=0.0, benchmark_cumulative_return=0.0),
        BenchmarkCurvePoint(point_id="2", created_at_utc="", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, timestamp="2024-01-02", simulated_benchmark_equity=101.0, benchmark_simple_return=0.01, benchmark_cumulative_return=0.01),
    ]
    b_series = BenchmarkReturnSeries(series_id="s1", created_at_utc="", benchmark_id="b1", benchmark_kind=BenchmarkKind.CASH_BASELINE, points=pts)

    alg = align_strategy_and_benchmark_returns(s_df, b_series, "r1")
    assert alg.alignment_valid is True
    assert len(alg.aligned_points) == 2
    assert alg.aligned_points[1].excess_return == pytest.approx(0.01)
