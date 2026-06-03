import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_comparison_reporting import (
    benchmark_comparison_context_to_text
)
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_comparison_report import build_benchmark_comparison_context

def test_reporting():
    ctx = build_benchmark_comparison_context()
    text = benchmark_comparison_context_to_text(ctx)
    assert "Context" in text
