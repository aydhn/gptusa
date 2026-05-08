import pytest
from pathlib import Path
from usa_signal_bot.regression.regression_store import (
    regression_store_dir, golden_store_dir, baseline_snapshot_dir,
    build_regression_run_dir, build_release_rehearsal_dir,
    write_regression_run_result_json, write_regression_step_results_jsonl,
    write_release_rehearsal_result_json, read_regression_run_result_json,
    read_release_rehearsal_result_json, list_regression_runs, list_release_rehearsals,
    get_latest_regression_run_dir, get_latest_release_rehearsal_dir, regression_store_summary
)
from usa_signal_bot.regression.regression_models import (
    RegressionRunResult, RegressionRunRequest, ReleaseRehearsalScope, RegressionRunStatus,
    ReleaseRehearsalResult, ReleaseCandidateStatus
)

def test_store_dirs(tmp_path):
    assert regression_store_dir(tmp_path).name == "regression"
    assert golden_store_dir(tmp_path).name == "golden"
    assert baseline_snapshot_dir(tmp_path).name == "baselines"

def test_write_read_run_result(tmp_path):
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden")
    res = RegressionRunResult(run_id="run1", created_at_utc="now", status=RegressionRunStatus.COMPLETED, request=req)

    run_dir = build_regression_run_dir(tmp_path, res.run_id)
    p = write_regression_run_result_json(run_dir / "result.json", res)
    assert p.exists()

    data = read_regression_run_result_json(p)
    assert data["run_id"] == "run1"

def test_write_read_release_result(tmp_path):
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden")
    reg_res = RegressionRunResult(run_id="run1", created_at_utc="now", status=RegressionRunStatus.COMPLETED, request=req)
    rel_res = ReleaseRehearsalResult(
        rehearsal_id="rel1", created_at_utc="now", scope=ReleaseRehearsalScope.SMOKE_ONLY,
        status=ReleaseCandidateStatus.PASSED, regression_result=reg_res
    )

    rel_dir = build_release_rehearsal_dir(tmp_path, rel_res.rehearsal_id)
    p = write_release_rehearsal_result_json(rel_dir / "rehearsal.json", rel_res)
    assert p.exists()

    data = read_release_rehearsal_result_json(p)
    assert data["rehearsal_id"] == "rel1"

def test_list_and_get_latest(tmp_path):
    assert len(list_regression_runs(tmp_path)) == 0
    assert get_latest_regression_run_dir(tmp_path) is None

    build_regression_run_dir(tmp_path, "run1").mkdir(parents=True)
    build_regression_run_dir(tmp_path, "run2").mkdir(parents=True)

    runs = list_regression_runs(tmp_path)
    assert len(runs) == 2
    assert get_latest_regression_run_dir(tmp_path) is not None

def test_regression_store_summary(tmp_path):
    build_regression_run_dir(tmp_path, "run1").mkdir(parents=True)
    summary = regression_store_summary(tmp_path)
    assert summary["runs_count"] == 1
    assert summary["releases_count"] == 0
