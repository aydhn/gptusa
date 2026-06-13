import sys
from unittest.mock import MagicMock

# Mock the enums to bypass ImportError during collection
sys.modules["usa_signal_bot.core.enums"] = MagicMock()

import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_schema_validator import (
    validate_benchmark_column_names,
)


def test_validate_benchmark_column_names_empty():
    assert validate_benchmark_column_names([]) == []


def test_validate_benchmark_column_names_valid():
    assert validate_benchmark_column_names(["date", "price", "volume"]) == []


def test_validate_benchmark_column_names_forbidden():
    assert validate_benchmark_column_names(["broker_order"]) == ["broker_order"]


def test_validate_benchmark_column_names_mixed():
    assert validate_benchmark_column_names(["date", "broker_order", "price"]) == [
        "broker_order"
    ]


def test_validate_benchmark_column_names_multiple_forbidden():
    assert validate_benchmark_column_names(
        ["broker_order", "price", "broker_order"]
    ) == ["broker_order", "broker_order"]
