import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.passive_benchmark_config import build_default_passive_benchmark_config
from usa_signal_bot.backtesting.benchmark_comparison.buy_and_hold_benchmark import build_buy_and_hold_benchmark_series

def test_build_buy_and_hold_benchmark():
    config = build_default_passive_benchmark_config()
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL"],
        "timestamp": ["2024-01-01", "2024-01-02"],
        "close": [100.0, 110.0]
    })
    series = build_buy_and_hold_benchmark_series(df, config, "AAPL")
    assert series.series_valid is True
    assert len(series.points) == 2
    assert series.points[0].simulated_benchmark_equity == 100000.0
    assert series.points[1].simulated_benchmark_equity == 110000.0
