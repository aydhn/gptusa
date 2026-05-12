import pytest
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, BaselineStatus, BaselineComparisonStatus, RuntimeRegressionStatus, BaselineDriftDirection, PerformanceReportType
from usa_signal_bot.performance.baseline_models import (
    PerformanceMetricBaseline, PerformanceBaseline, CurrentPerformanceSample, BaselineComparisonResult, PerformanceReviewResult,
    create_performance_metric_baseline_id, create_performance_baseline_id, create_current_performance_sample_id,
    create_baseline_comparison_id, create_performance_review_id,
    validate_performance_metric_baseline, validate_performance_baseline, validate_current_performance_sample, validate_baseline_comparison_result,
    performance_metric_baseline_to_dict, performance_baseline_to_dict, current_performance_sample_to_dict, baseline_comparison_result_to_dict, performance_review_result_to_dict
)
from usa_signal_bot.core.exceptions import PerformanceBaselineValidationError

def test_performance_metric_baseline_valid():
    metric = PerformanceMetricBaseline(
        metric_id="m1", name=PerformanceMetricName.WALL_TIME_SECONDS, scope=PerformanceBaselineScope.SCAN,
        sample_count=10, mean_value=1.5, median_value=1.0, p75_value=2.0, p90_value=3.0, min_value=0.5, max_value=5.0,
        unit="s", status=BaselineStatus.ACTIVE, metadata={}
    )
    validate_performance_metric_baseline(metric)
    assert metric.sample_count == 10

def test_performance_metric_baseline_invalid_negative():
    metric = PerformanceMetricBaseline(
        metric_id="m1", name=PerformanceMetricName.WALL_TIME_SECONDS, scope=PerformanceBaselineScope.SCAN,
        sample_count=10, mean_value=-1.5, median_value=1.0, p75_value=2.0, p90_value=3.0, min_value=0.5, max_value=5.0,
        unit="s", status=BaselineStatus.ACTIVE, metadata={}
    )
    with pytest.raises(PerformanceBaselineValidationError):
        validate_performance_metric_baseline(metric)

def test_performance_baseline_valid():
    b = PerformanceBaseline(
        baseline_id="b1", version="v1", scope=PerformanceBaselineScope.SCAN, status=BaselineStatus.ACTIVE,
        created_at_utc=datetime.now(timezone.utc).isoformat(), source_count=5, metrics=[], source_paths=[], warnings=[], errors=[]
    )
    validate_performance_baseline(b)

def test_current_performance_sample_serialization():
    s = CurrentPerformanceSample(
        sample_id="s1", scope=PerformanceBaselineScope.SCAN, created_at_utc=datetime.now(timezone.utc).isoformat(),
        metrics={PerformanceMetricName.WALL_TIME_SECONDS.value: 10}, source_path=None, warnings=[], errors=[], metadata={}
    )
    validate_current_performance_sample(s)
    d = current_performance_sample_to_dict(s)
    assert d["sample_id"] == "s1"
    assert d["metrics"]["WALL_TIME_SECONDS"] == 10

def test_id_factories_not_empty():
    assert create_performance_metric_baseline_id(PerformanceMetricName.WALL_TIME_SECONDS, PerformanceBaselineScope.SCAN)
    assert create_performance_baseline_id(PerformanceBaselineScope.SCAN)
    assert create_current_performance_sample_id(PerformanceBaselineScope.SCAN)
    assert create_baseline_comparison_id()
    assert create_performance_review_id()
