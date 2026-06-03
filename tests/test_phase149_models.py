import pytest
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import (
    BacktestAnalyticsIngestionResult,
    BenchmarkInputReference,
    BenchmarkUniverseContract,
    PassiveBenchmarkConfig,
    create_backtest_analytics_ingestion_id,
    create_benchmark_input_reference_id
)

def test_models_creation():
    ingestion_id = create_backtest_analytics_ingestion_id()
    assert ingestion_id.startswith("btai-")

    ref_id = create_benchmark_input_reference_id()
    assert ref_id.startswith("bmin-")
