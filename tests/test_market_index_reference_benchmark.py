import pytest
import pandas as pd
from usa_signal_bot.backtesting.benchmark_comparison.passive_benchmark_config import build_default_passive_benchmark_config
from usa_signal_bot.backtesting.benchmark_comparison.market_index_reference_benchmark import build_market_index_reference_benchmark_series

def test_build_market_index_benchmark():
    config = build_default_passive_benchmark_config()
    df = pd.DataFrame({
        "timestamp": ["2024-01-01", "2024-01-02"],
        "close": [400.0, 420.0]
    })
    series = build_market_index_reference_benchmark_series(df, config, "SPY")
    assert series.series_valid is True
    assert len(series.points) == 2
