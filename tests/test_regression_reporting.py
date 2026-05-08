import pytest
from usa_signal_bot.regression.regression_reporting import (
    golden_dataset_spec_to_text,
    golden_snapshot_to_text,
    regression_step_result_to_text,
    regression_run_result_to_text,
    release_rehearsal_result_to_text,
    snapshot_comparison_to_text,
    regression_store_summary_to_text,
    regression_limitations_text,
    write_regression_report_json,
    write_release_rehearsal_report_json
)
from usa_signal_bot.regression.regression_models import (
    GoldenDatasetSpec, GoldenDatasetStatus, GoldenSnapshot, RegressionArtifactType,
    RegressionStepResult, RegressionStepName, RegressionStepStatus,
    RegressionRunRequest, ReleaseRehearsalScope, RegressionRunResult, RegressionRunStatus,
    ReleaseRehearsalResult, ReleaseCandidateStatus
)

def test_reporting_formatting():
    spec = GoldenDatasetSpec("ds1", "gold", ["AAPL"], "1d", "start", "end", 10, GoldenDatasetStatus.VALID, "now")
    assert "gold" in golden_dataset_spec_to_text(spec)

    snap = GoldenSnapshot("s1", "snap1", RegressionArtifactType.SNAPSHOT, "now", "1234", {})
    assert "snap1" in golden_snapshot_to_text(snap)

    step = RegressionStepResult(RegressionStepName.FEATURE_REHEARSAL, RegressionStepStatus.PASSED, duration_seconds=1.5)
    assert "FEATURE_REHEARSAL" in regression_step_result_to_text(step)

    req = RegressionRunRequest("r1", ReleaseRehearsalScope.SMOKE_ONLY, "gold")
    run_res = RegressionRunResult("run1", "now", RegressionRunStatus.COMPLETED, req, step_results=[step])
    run_txt = regression_run_result_to_text(run_res)
    assert "run1" in run_txt
    assert "COMPLETED" in run_txt

    rel_res = ReleaseRehearsalResult("rel1", "now", ReleaseRehearsalScope.SMOKE_ONLY, ReleaseCandidateStatus.PASSED, run_res)
    rel_txt = release_rehearsal_result_to_text(rel_res)
    assert "rel1" in rel_txt
    assert "PASSED" in rel_txt

    assert "MATCH" in snapshot_comparison_to_text({"status": "MATCH"})
    assert "1 Runs" in regression_store_summary_to_text({"runs_count": 1})
    assert "NOT an approval" in regression_limitations_text()

def test_write_reports(tmp_path):
    req = RegressionRunRequest("r1", ReleaseRehearsalScope.SMOKE_ONLY, "gold")
    run_res = RegressionRunResult("run1", "now", RegressionRunStatus.COMPLETED, req)
    p = write_regression_report_json(tmp_path / "run.json", run_res)
    assert p.exists()

    rel_res = ReleaseRehearsalResult("rel1", "now", ReleaseRehearsalScope.SMOKE_ONLY, ReleaseCandidateStatus.PASSED, run_res)
    p2 = write_release_rehearsal_report_json(tmp_path / "rel.json", rel_res)
    assert p2.exists()
