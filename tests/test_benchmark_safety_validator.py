import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_safety_validator import (
    benchmark_text_has_trade_or_execution_language
)

def test_safety_validator():
    assert benchmark_text_has_trade_or_execution_language("This is a diagnostic metric.") is False
    assert benchmark_text_has_trade_or_execution_language("I definitely buy this asset.") is True
