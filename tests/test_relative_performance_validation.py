import pytest
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BaselineComparisonReport
from usa_signal_bot.backtesting.benchmark_comparison.relative_performance_validation import build_relative_performance_validation_report

def test_build_relative_validation():
    report = BaselineComparisonReport(report_id="r1", created_at_utc="", run_id="run1")
    val = build_relative_performance_validation_report(report)
    assert val.validation_passed is False # rules will fail because lists are empty
