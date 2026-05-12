import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineComparisonStatus, PerformanceReportType
from usa_signal_bot.performance.baseline_models import PerformanceReviewResult
from usa_signal_bot.performance.profiling_adapter import performance_samples_from_resource_profiles, performance_baseline_from_resource_profiles, profiling_calibration_hints_from_performance_review

def test_performance_samples_from_resource_profiles():
    class DummyProfile:
        def __init__(self):
            self.scope = "SCAN"
            self.metrics = {"wall_time_seconds": 10.0}
    p = DummyProfile()
    s = performance_samples_from_resource_profiles([p, {"scope": "PAPER", "metrics": {"wall_time_seconds": 20.0}}])
    assert len(s) == 2
    assert s[0].scope == PerformanceBaselineScope.SCAN
    assert s[1].scope == PerformanceBaselineScope.PAPER

def test_performance_baseline_from_resource_profiles():
    b = performance_baseline_from_resource_profiles(PerformanceBaselineScope.SCAN, [{"scope": "SCAN", "metrics": {"wall_time_seconds": 10.0}}])
    assert b.scope == PerformanceBaselineScope.SCAN

def test_profiling_calibration_hints_from_performance_review():
    rev = PerformanceReviewResult("r1", "", PerformanceReportType.FULL_PERFORMANCE_REVIEW, BaselineComparisonStatus.FAIL, [], [], [], [], [], BaselineComparisonStatus.FAIL, {}, [], [])
    hints = profiling_calibration_hints_from_performance_review(rev)
    assert hints["action"] == "REDUCE_SCOPE"
    assert "FAIL" in hints["reason"]
