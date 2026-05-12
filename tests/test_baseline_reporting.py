import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineStatus, BaselineComparisonStatus, PerformanceReportType
from usa_signal_bot.performance.baseline_models import PerformanceMetricBaseline, PerformanceMetricName, PerformanceBaseline, PerformanceReviewResult
from usa_signal_bot.performance.baseline_reporting import (
    performance_metric_baseline_to_text, performance_baseline_to_text, performance_review_result_to_text, performance_baseline_limitations_text
)

def test_performance_metric_baseline_to_text():
    m = PerformanceMetricBaseline("m1", PerformanceMetricName.WALL_TIME_SECONDS, PerformanceBaselineScope.SCAN, 10, 10, 10, 10, 15, 5, 20, None, BaselineStatus.ACTIVE, {})
    txt = performance_metric_baseline_to_text(m)
    assert "WALL_TIME_SECONDS:" in txt
    assert "p90=15.00" in txt

def test_performance_baseline_to_text():
    b = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    txt = performance_baseline_to_text(b)
    assert "Performance Baseline: SCAN (v: v1)" in txt

def test_performance_review_result_to_text():
    rev = PerformanceReviewResult("r1", "", PerformanceReportType.FULL_PERFORMANCE_REVIEW, BaselineComparisonStatus.PASS, [], [], [], [], [], BaselineComparisonStatus.PASS, {}, [], [])
    txt = performance_review_result_to_text(rev)
    assert "PERFORMANCE REVIEW RESULT: PASS" in txt

def test_performance_baseline_limitations_text():
    txt = performance_baseline_limitations_text()
    assert "no external telemetry" in txt.lower()
    assert "not an approval for live trading" in txt.lower() or "not a live trading approval" in txt.lower()
