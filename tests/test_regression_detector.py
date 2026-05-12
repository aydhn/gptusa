import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample
from usa_signal_bot.performance.regression_detector import RuntimeRegressionDetector

def test_regression_detector():
    s = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 100}, None, [], [], {})
    det = RuntimeRegressionDetector([], [])

    comp, rep = det.detect(s)
    assert comp.sample_id == "s1"
    assert rep.scope == PerformanceBaselineScope.SCAN

def test_regression_detector_detect_many():
    s1 = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 100}, None, [], [], {})
    s2 = CurrentPerformanceSample("s2", PerformanceBaselineScope.PAPER, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 100}, None, [], [], {})

    det = RuntimeRegressionDetector([], [])
    res = det.detect_many([s1, s2])
    assert len(res) == 2

def test_regression_detector_summarize():
    s1 = CurrentPerformanceSample("s1", PerformanceBaselineScope.SCAN, "", {PerformanceMetricName.WALL_TIME_SECONDS.value: 100}, None, [], [], {})
    det = RuntimeRegressionDetector([], [])
    res = det.detect_many([s1])

    sum = det.summarize_regressions(res)
    assert sum["total_checked"] == 1
    assert sum["insufficient_data"] == 0
    assert sum["no_regression"] == 1 # defaults to insufficient because no baseline provided
