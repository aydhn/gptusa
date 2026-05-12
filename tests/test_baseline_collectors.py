import pytest
from pathlib import Path
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName
from usa_signal_bot.performance.baseline_collectors import (
    normalize_profile_to_sample, normalize_regression_result_to_sample,
    normalize_scheduler_result_to_sample, normalize_taskqueue_result_to_sample, normalize_quality_result_to_sample,
    collect_current_operational_sample, _redact_secrets
)

def test_normalize_profile_to_sample():
    p = {
        "scope": "SCAN",
        "metrics": {"wall_time_seconds": 5.0, "memory_peak_bytes": 1048576},
        "created_at_utc": "2023-01-01"
    }
    s = normalize_profile_to_sample(p)
    assert s.scope == PerformanceBaselineScope.SCAN
    assert s.metrics[PerformanceMetricName.WALL_TIME_SECONDS.value] == 5.0
    assert s.metrics[PerformanceMetricName.MEMORY_PEAK_MB.value] == 1.0

def test_normalize_regression_result_to_sample():
    p = {"duration_seconds": 10.0, "error_count": 0}
    s = normalize_regression_result_to_sample(p)
    assert s.scope == PerformanceBaselineScope.REGRESSION
    assert s.metrics[PerformanceMetricName.WALL_TIME_SECONDS.value] == 10.0

def test_normalize_scheduler_result_to_sample():
    s = normalize_scheduler_result_to_sample({})
    assert s.scope == PerformanceBaselineScope.SCHEDULER

def test_normalize_taskqueue_result_to_sample():
    s = normalize_taskqueue_result_to_sample({})
    assert s.scope == PerformanceBaselineScope.TASKQUEUE

def test_normalize_quality_result_to_sample():
    s = normalize_quality_result_to_sample({})
    assert s.scope == PerformanceBaselineScope.QUALITY

def test_collect_current_operational_sample():
    s = collect_current_operational_sample(Path("/dummy"))
    assert s.scope == PerformanceBaselineScope.FULL_LOCAL_STACK

def test_redact_secrets():
    data = {"normal": 1, "my_api_key": "12345", "nested": {"password": "abc"}}
    r = _redact_secrets(data)
    assert r["normal"] == 1
    assert r["my_api_key"] == "***REDACTED***"
    assert r["nested"]["password"] == "***REDACTED***"
