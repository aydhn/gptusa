import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, BaselineStatus
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample
from usa_signal_bot.performance.baseline_builder import (
    metric_values_from_samples, calculate_percentile, build_metric_baseline, build_performance_baseline, build_all_performance_baselines, baseline_builder_summary_to_text
)

def test_metric_values_from_samples():
    s1 = CurrentPerformanceSample("1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 10}, None, [], [], {})
    s2 = CurrentPerformanceSample("2", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 20}, None, [], [], {})
    s3 = CurrentPerformanceSample("3", PerformanceBaselineScope.SCAN, "", {"UNKNOWN": 30}, None, [], [], {})

    vals = metric_values_from_samples([s1, s2, s3], PerformanceMetricName.WALL_TIME_SECONDS)
    assert len(vals) == 2
    assert 10.0 in vals

def test_calculate_percentile():
    vals = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert calculate_percentile(vals, 50) == 3.0
    assert calculate_percentile(vals, 100) == 5.0
    assert calculate_percentile([], 50) is None

def test_build_metric_baseline():
    b = build_metric_baseline(PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, [10, 20, 30])
    assert b.status == BaselineStatus.ACTIVE
    assert b.mean_value == 20.0
    assert b.p90_value > 20.0

def test_build_metric_baseline_insufficient():
    b = build_metric_baseline(PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, [10])
    assert b.status == BaselineStatus.INSUFFICIENT_DATA

def test_build_performance_baseline():
    s1 = CurrentPerformanceSample("1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 10}, None, [], [], {})
    s2 = CurrentPerformanceSample("2", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 20}, None, [], [], {})
    s3 = CurrentPerformanceSample("3", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 30}, None, [], [], {})

    b = build_performance_baseline(PerformanceBaselineScope.SCAN, [s1, s2, s3])
    assert b.scope == PerformanceBaselineScope.SCAN
    assert b.status == BaselineStatus.ACTIVE
    assert len(b.metrics) == 1

def test_build_all_performance_baselines():
    s1 = CurrentPerformanceSample("1", PerformanceBaselineScope.SCAN, "", {}, None, [], [], {})
    s2 = CurrentPerformanceSample("2", PerformanceBaselineScope.PAPER, "", {}, None, [], [], {})
    bs = build_all_performance_baselines([s1, s2])
    assert len(bs) == 2

def test_baseline_builder_summary_to_text():
    b = build_performance_baseline(PerformanceBaselineScope.SCAN, [])
    txt = baseline_builder_summary_to_text([b])
    assert "Total Baselines Built: 1" in txt
