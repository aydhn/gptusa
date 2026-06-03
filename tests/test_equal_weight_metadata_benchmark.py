import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.passive_benchmark_config import build_default_passive_benchmark_config
from usa_signal_bot.backtesting.benchmark_comparison.equal_weight_metadata_benchmark import build_equal_weight_metadata_benchmark_series

def test_build_equal_weight_benchmark():
    config = build_default_passive_benchmark_config()
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "MSFT", "MSFT"],
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02"],
        "close": [100.0, 110.0, 200.0, 210.0]
    })
    series = build_equal_weight_metadata_benchmark_series(df, config)
    assert series.series_valid is True
    assert len(series.points) == 2
