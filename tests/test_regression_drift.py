import pytest
from usa_signal_bot.regression.regression_models import SnapshotComparisonStatus, RegressionDriftSeverity
from usa_signal_bot.regression.regression_drift import build_regression_drift_report, classify_regression_drift_severity, regression_drift_report_to_text

def test_build_regression_drift_report_no_diff():
    snapshot_results = {
        "step1": {"status": "MATCH"}
    }
    report = build_regression_drift_report(snapshot_results)
    assert report.status == SnapshotComparisonStatus.MATCH
    assert report.drift_count == 0

def test_build_regression_drift_report_drift():
    snapshot_results = {
        "step1": {
            "status": "DRIFT",
            "diff_summary": {"details": ["status field changed"]}
        }
    }
    report = build_regression_drift_report(snapshot_results)
    assert report.status == SnapshotComparisonStatus.DRIFT
    assert report.drift_count == 1
    assert report.max_severity == RegressionDriftSeverity.HIGH

def test_classify_regression_drift_severity():
    sev1 = classify_regression_drift_severity({"details": ["count changed"]})
    assert sev1 == RegressionDriftSeverity.HIGH

    sev2 = classify_regression_drift_severity({"details": ["feature1 changed"]})
    assert sev2 == RegressionDriftSeverity.LOW

    sev3 = classify_regression_drift_severity({})
    assert sev3 == RegressionDriftSeverity.NONE

def test_regression_drift_report_to_text():
    snapshot_results = {
        "step1": {"status": "DRIFT", "diff_summary": {"details": ["count changed"]}}
    }
    report = build_regression_drift_report(snapshot_results)
    text = regression_drift_report_to_text(report)
    assert "Status: DRIFT" in text
    assert "count changed" in text
