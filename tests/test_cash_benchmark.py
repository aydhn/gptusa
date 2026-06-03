import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.passive_benchmark_config import build_default_passive_benchmark_config
from usa_signal_bot.backtesting.benchmark_comparison.cash_benchmark import build_cash_benchmark_series

def test_build_cash_benchmark():
    config = build_default_passive_benchmark_config()
    df = pd.DataFrame({"timestamp": ["2024-01-01", "2024-01-02"]})
    series = build_cash_benchmark_series(df, config)
    assert series.series_valid is True
    assert len(series.points) == 2
    assert series.points[0].simulated_benchmark_equity == 100000.0
