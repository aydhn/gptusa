import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, BaselineComparisonStatus, BaselineStatus
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample, PerformanceBaseline, PerformanceMetricBaseline
from usa_signal_bot.performance.baseline_comparator import (
    calculate_delta_pct, compare_metric_to_baseline, classify_comparison_status, find_baseline_for_sample, compare_sample_to_baseline, baseline_comparison_result_to_text
)

def test_calculate_delta_pct():
    assert calculate_delta_pct(150, 100) == 50.0
    assert calculate_delta_pct(100, 100) == 0.0
    assert calculate_delta_pct(None, 100) is None
    assert calculate_delta_pct(100, 0) is None

def test_compare_metric_to_baseline():
    mb = PerformanceMetricBaseline("m1", PerformanceMetricName.WALL_TIME_SECONDS, PerformanceBaselineScope.SCAN, 10, 100, 100, 110, 100, 90, 120, None, BaselineStatus.ACTIVE, {})
    res = compare_metric_to_baseline(PerformanceMetricName.WALL_TIME_SECONDS, 100, mb)
    assert res["status"] == BaselineComparisonStatus.PASS

    res_warn = compare_metric_to_baseline(PerformanceMetricName.WALL_TIME_SECONDS, 130, mb) # 30% diff
    assert res_warn["status"] == BaselineComparisonStatus.WARN

    res_fail = compare_metric_to_baseline(PerformanceMetricName.WALL_TIME_SECONDS, 160, mb) # 60% diff
    assert res_fail["status"] == BaselineComparisonStatus.FAIL

    res_block = compare_metric_to_baseline(PerformanceMetricName.WALL_TIME_SECONDS, 250, mb) # 150% diff
    assert res_block["status"] == BaselineComparisonStatus.BLOCKED

def test_compare_metric_errors():
    mb = PerformanceMetricBaseline("m1", PerformanceMetricName.ERROR_COUNT, PerformanceBaselineScope.SCAN, 10, 1, 1, 1, 1, 0, 2, None, BaselineStatus.ACTIVE, {})
    res = compare_metric_to_baseline(PerformanceMetricName.ERROR_COUNT, 2, mb) # > 1
    assert res["status"] == BaselineComparisonStatus.FAIL
    res2 = compare_metric_to_baseline(PerformanceMetricName.ERROR_COUNT, 3, mb) # > 2
    assert res2["status"] == BaselineComparisonStatus.BLOCKED

def test_find_baseline_for_sample():
    b = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {}, None, [], [], {})
    assert find_baseline_for_sample(s, [b]) == b

def test_compare_sample_to_baseline():
    b = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 100}, None, [], [], {})
    res = compare_sample_to_baseline(s, b)
    assert res.status == BaselineComparisonStatus.INSUFFICIENT_DATA # b has no metrics
    txt = baseline_comparison_result_to_text(res)
    assert "Baseline Comparison" in txt
