import pytest
from usa_signal_bot.regression.regression_validation import (
    validate_regression_run_result_report,
    validate_release_rehearsal_result_report,
    validate_golden_dataset_files,
    validate_snapshot_comparison_payload,
    validate_no_live_execution_in_regression,
    validate_no_investment_advice_language_in_regression,
    assert_regression_valid
)
from usa_signal_bot.regression.regression_models import (
    RegressionRunResult, RegressionRunRequest, ReleaseRehearsalScope, RegressionRunStatus,
    RegressionStepResult, RegressionStepName, RegressionStepStatus,
    ReleaseRehearsalResult, ReleaseCandidateStatus
)
from usa_signal_bot.core.exceptions import RegressionValidationError

def test_validate_regression_run_result_report():
    step = RegressionStepResult(step_name=RegressionStepName.FEATURE_REHEARSAL, status=RegressionStepStatus.PASSED, duration_seconds=-1.0)
    req = RegressionRunRequest(request_id="r1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="gold")
    res = RegressionRunResult(run_id="run1", created_at_utc="now", status=RegressionRunStatus.COMPLETED, request=req, step_results=[step])

    report = validate_regression_run_result_report(res)
    assert not report.valid
    assert len(report.errors) == 1

def test_validate_release_rehearsal_result_report():
    req = RegressionRunRequest(request_id="r1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="gold")
    reg_res = RegressionRunResult(run_id="run1", created_at_utc="now", status=RegressionRunStatus.COMPLETED, request=req)
    rel_res = ReleaseRehearsalResult(
        rehearsal_id="rel1", created_at_utc="now", scope=ReleaseRehearsalScope.SMOKE_ONLY,
        status=ReleaseCandidateStatus.PASSED, regression_result=reg_res, failed_steps=1
    )

    report = validate_release_rehearsal_result_report(rel_res)
    assert not report.valid

def test_validate_golden_dataset_files(tmp_path):
    report = validate_golden_dataset_files(tmp_path)
    assert not report.valid
    assert len(report.errors) == 5

def test_validate_snapshot_comparison_payload():
    report = validate_snapshot_comparison_payload({"status": "INVALID", "message": "error"})
    assert not report.valid

    report2 = validate_snapshot_comparison_payload({"status": "MATCH"})
    assert report2.valid

def test_validate_no_live_execution():
    report = validate_no_live_execution_in_regression({"some_field": "test", "another": "live_order_id"})
    assert not report.valid

    report2 = validate_no_live_execution_in_regression({"status": "PASSED"})
    assert report2.valid

def test_validate_no_investment_advice():
    report = validate_no_investment_advice_language_in_regression("This is kesin al for sure.")
    assert not report.valid

    report2 = validate_no_investment_advice_language_in_regression("This is a local regression test.")
    assert report2.valid

def test_assert_regression_valid():
    report = validate_snapshot_comparison_payload({"status": "INVALID", "message": "error"})
    with pytest.raises(RegressionValidationError):
        assert_regression_valid(report)
