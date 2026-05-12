import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, BaselineComparisonStatus, SLAThresholdType, SLASeverity
from usa_signal_bot.performance.threshold_models import SLAThreshold
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample
from usa_signal_bot.performance.threshold_evaluator import (
    default_sla_thresholds, thresholds_for_scope, evaluate_threshold, evaluate_thresholds, sla_evaluation_report_to_text
)

def test_default_sla_thresholds():
    ts = default_sla_thresholds()
    assert len(ts) > 0

def test_thresholds_for_scope():
    ts = thresholds_for_scope(PerformanceBaselineScope.SCAN)
    assert any(t.scope == PerformanceBaselineScope.SCAN for t in ts)

def test_evaluate_threshold_pass():
    t = SLAThreshold("t1", "t", PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 10, 20, 30, True, SLASeverity.WARNING)
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 5}, None, [], [], {})
    res = evaluate_threshold(t, s, None)
    assert res.status == BaselineComparisonStatus.PASS

def test_evaluate_threshold_warn():
    t = SLAThreshold("t1", "t", PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 10, 20, 30, True, SLASeverity.WARNING)
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 15}, None, [], [], {})
    res = evaluate_threshold(t, s, None)
    assert res.status == BaselineComparisonStatus.WARN

def test_evaluate_threshold_fail():
    t = SLAThreshold("t1", "t", PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 10, 20, 30, True, SLASeverity.WARNING)
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 25}, None, [], [], {})
    res = evaluate_threshold(t, s, None)
    assert res.status == BaselineComparisonStatus.FAIL

def test_evaluate_threshold_blocked():
    t = SLAThreshold("t1", "t", PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 10, 20, 30, True, SLASeverity.WARNING)
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 35}, None, [], [], {})
    res = evaluate_threshold(t, s, None)
    assert res.status == BaselineComparisonStatus.BLOCKED

def test_evaluate_threshold_insufficient():
    t = SLAThreshold("t1", "t", PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 10, 20, 30, True, SLASeverity.WARNING)
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {}, None, [], [], {})
    res = evaluate_threshold(t, s, None)
    assert res.status == BaselineComparisonStatus.INSUFFICIENT_DATA

def test_evaluate_thresholds():
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 3500}, None, [], [], {})
    rep = evaluate_thresholds(PerformanceBaselineScope.SCAN, s, None)
    assert rep.status in [BaselineComparisonStatus.WARN, BaselineComparisonStatus.FAIL, BaselineComparisonStatus.BLOCKED] # depending on default

def test_sla_evaluation_report_to_text():
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 5}, None, [], [], {})
    rep = evaluate_thresholds(PerformanceBaselineScope.SCAN, s, None)
    txt = sla_evaluation_report_to_text(rep)
    assert "SLA PASS is not an approval for live trading" in txt
