import pytest
from usa_signal_bot.regression.regression_models import (
    GoldenDatasetSpec, GoldenDatasetStatus, GoldenSnapshot, RegressionArtifactType,
    RegressionStepResult, RegressionStepName, RegressionStepStatus,
    RegressionRunRequest, ReleaseRehearsalScope, RegressionRunResult, RegressionRunStatus,
    ReleaseCandidateStatus, ReleaseRehearsalResult,
    golden_dataset_spec_to_dict, regression_step_result_to_dict, regression_run_request_to_dict,
    regression_run_result_to_dict, release_rehearsal_result_to_dict,
    create_golden_dataset_id, create_golden_snapshot_id, create_regression_request_id,
    create_regression_run_id, create_release_rehearsal_id,
    validate_golden_dataset_spec
)

def test_golden_dataset_spec_creation():
    spec = GoldenDatasetSpec(
        dataset_id="test_id", name="test", symbols=["AAPL"], timeframe="1d",
        start_date="2024-01-01", end_date="2024-01-02", row_count_per_symbol=10,
        status=GoldenDatasetStatus.CREATED, created_at_utc="now"
    )
    assert spec.name == "test"
    validate_golden_dataset_spec(spec)

def test_invalid_empty_symbols_error():
    spec = GoldenDatasetSpec(
        dataset_id="test_id", name="test", symbols=[], timeframe="1d",
        start_date="2024-01-01", end_date="2024-01-02", row_count_per_symbol=10,
        status=GoldenDatasetStatus.CREATED, created_at_utc="now"
    )
    with pytest.raises(ValueError):
        validate_golden_dataset_spec(spec)

def test_golden_snapshot_valid_creation():
    snap = GoldenSnapshot(
        snapshot_id="s1", name="test_snap", artifact_type=RegressionArtifactType.SNAPSHOT,
        created_at_utc="now", checksum="1234", payload={"data": 1}
    )
    assert snap.checksum == "1234"

def test_regression_step_result_serialize():
    step = RegressionStepResult(
        step_name=RegressionStepName.FEATURE_REHEARSAL,
        status=RegressionStepStatus.PASSED,
        duration_seconds=1.5
    )
    d = regression_step_result_to_dict(step)
    assert d["step_name"] == "FEATURE_REHEARSAL"
    assert d["status"] == "PASSED"
    assert d["duration_seconds"] == 1.5

def test_regression_run_request_valid_creation():
    req = RegressionRunRequest(
        request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden"
    )
    assert req.scope == ReleaseRehearsalScope.SMOKE_ONLY

def test_regression_run_result_serialize():
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden")
    res = RegressionRunResult(run_id="run1", created_at_utc="now", status=RegressionRunStatus.NOT_STARTED, request=req)
    d = regression_run_result_to_dict(res)
    assert d["run_id"] == "run1"
    assert d["request"]["scope"] == "SMOKE_ONLY"

def test_release_rehearsal_result_serialize():
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden")
    reg_res = RegressionRunResult(run_id="run1", created_at_utc="now", status=RegressionRunStatus.COMPLETED, request=req)
    rel_res = ReleaseRehearsalResult(
        rehearsal_id="rel1", created_at_utc="now", scope=ReleaseRehearsalScope.SMOKE_ONLY,
        status=ReleaseCandidateStatus.PASSED, regression_result=reg_res
    )
    d = release_rehearsal_result_to_dict(rel_res)
    assert d["rehearsal_id"] == "rel1"
    assert d["status"] == "PASSED"

def test_id_factory_generates_non_empty_ids():
    assert create_golden_dataset_id()
    assert create_golden_snapshot_id("test")
    assert create_regression_request_id()
    assert create_regression_run_id()
    assert create_release_rehearsal_id()
