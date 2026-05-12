import pytest
from usa_signal_bot.core.enums import BaselineDriftDirection, RuntimeRegressionStatus, BaselineComparisonStatus
from usa_signal_bot.performance.drift_classifier import (
    classify_baseline_drift, classify_runtime_regression, drift_score_from_metric_results, summarize_drift_reasons
)

def test_classify_baseline_drift_better():
    res = [{"delta_pct": -10.0}, {"delta_pct": -6.0}]
    assert classify_baseline_drift(res) == BaselineDriftDirection.BETTER

def test_classify_baseline_drift_worse():
    res = [{"delta_pct": 10.0}, {"delta_pct": 6.0}]
    assert classify_baseline_drift(res) == BaselineDriftDirection.WORSE

def test_classify_baseline_drift_mixed():
    res = [{"delta_pct": 10.0}, {"delta_pct": -6.0}]
    assert classify_baseline_drift(res) == BaselineDriftDirection.MIXED

def test_classify_baseline_drift_flat():
    res = [{"delta_pct": 1.0}, {"delta_pct": -1.0}]
    assert classify_baseline_drift(res) == BaselineDriftDirection.FLAT

def test_classify_runtime_regression():
    res_crit = [{"status": BaselineComparisonStatus.BLOCKED.value}]
    assert classify_runtime_regression(res_crit) == RuntimeRegressionStatus.CRITICAL_REGRESSION

    res_major = [{"status": BaselineComparisonStatus.FAIL.value}]
    assert classify_runtime_regression(res_major) == RuntimeRegressionStatus.MAJOR_REGRESSION

    res_mod = [{"status": BaselineComparisonStatus.WARN.value}]
    assert classify_runtime_regression(res_mod) == RuntimeRegressionStatus.MODERATE_REGRESSION

    res_min = [{"status": BaselineComparisonStatus.PASS.value, "delta_pct": 10.0}]
    assert classify_runtime_regression(res_min) == RuntimeRegressionStatus.MINOR_REGRESSION

    res_no = [{"status": BaselineComparisonStatus.PASS.value, "delta_pct": 1.0}]
    assert classify_runtime_regression(res_no) == RuntimeRegressionStatus.NO_REGRESSION

def test_drift_score_from_metric_results():
    res = [{"delta_pct": 10.0}, {"delta_pct": -5.0}, {}]
    assert drift_score_from_metric_results(res) == 2.5

def test_summarize_drift_reasons():
    res = [{"metric_name": "WALL_TIME_SECONDS", "delta_pct": 10.0}, {"metric_name": "MEMORY_PEAK_MB", "delta_pct": -10.0}]
    reasons = summarize_drift_reasons(res)
    assert len(reasons) == 2
    assert "WALL_TIME_SECONDS increased by 10.0%" in reasons[0]
