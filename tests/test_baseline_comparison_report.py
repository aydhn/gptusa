import pytest
from usa_signal_bot.backtesting.benchmark_comparison.baseline_comparison_report import build_baseline_comparison_report

def test_build_baseline_report():
    report = build_baseline_comparison_report("r1", [], [], [], [])
    assert report.report_valid is False # invalid if empty
