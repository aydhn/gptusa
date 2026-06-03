import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_comparison_report import (
    build_benchmark_comparison_context,
    build_benchmark_comparison_full_review
)

def test_build_report():
    ctx = build_benchmark_comparison_context()
    assert ctx.context_id is not None

    rev = build_benchmark_comparison_full_review()
    assert rev.review_id is not None
