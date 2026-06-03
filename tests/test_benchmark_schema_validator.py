import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_schema_validator import (
    validate_benchmark_column_names
)

def test_schema_validator():
    errors = validate_benchmark_column_names(["timestamp", "close"])
    assert len(errors) == 0

    errors_bad = validate_benchmark_column_names(["timestamp", "broker_order"])
    assert len(errors_bad) == 1
