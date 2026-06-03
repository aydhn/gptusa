import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_return_series import (
    build_benchmark_curve_points_from_equity
)
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkKind

def test_build_curve_points():
    df = pd.DataFrame({
        "timestamp": ["2024-01-01", "2024-01-02"],
        "simulated_benchmark_equity": [100.0, 105.0]
    })
    points = build_benchmark_curve_points_from_equity("bm-1", BenchmarkKind.CASH_BASELINE, df)
    assert len(points) == 2
    assert points[1].benchmark_simple_return == 0.05
