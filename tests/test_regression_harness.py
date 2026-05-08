import pytest
from usa_signal_bot.regression.regression_harness import EndToEndRegressionHarness
from usa_signal_bot.regression.regression_models import RegressionRunRequest, ReleaseRehearsalScope, RegressionRunStatus
from usa_signal_bot.regression.regression_steps import RegressionStepName

def test_build_step_plan(tmp_path):
    harness = EndToEndRegressionHarness(tmp_path)
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden")

    plan = harness.build_step_plan(req)
    assert RegressionStepName.GENERATE_GOLDEN_FIXTURES in plan
    assert RegressionStepName.PAPER_DRY_RUN_REHEARSAL in plan
    assert RegressionStepName.FEATURE_REHEARSAL not in plan

    req_golden = RegressionRunRequest(request_id="req2", scope=ReleaseRehearsalScope.GOLDEN_SAMPLE, dataset_name="golden")
    plan_golden = harness.build_step_plan(req_golden)
    assert len(plan_golden) > len(plan)

def test_run_smoke_only(tmp_path):
    harness = EndToEndRegressionHarness(tmp_path)
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden", write_outputs=False)

    result = harness.run(req)
    assert result.status in (RegressionRunStatus.COMPLETED, RegressionRunStatus.PARTIAL_SUCCESS)
    assert len(result.step_results) > 0

def test_fail_on_drift(tmp_path):
    harness = EndToEndRegressionHarness(tmp_path)
    # create baseline
    from usa_signal_bot.regression.golden_snapshots import create_golden_snapshot, write_or_update_baseline_snapshot
    snap = create_golden_snapshot("risk_rehearsal", {"items": ["diff_data"]})
    write_or_update_baseline_snapshot(harness.baseline_dir, snap)

    # run with fail_on_drift and compare_snapshots
    req = RegressionRunRequest(request_id="req1", scope=ReleaseRehearsalScope.SMOKE_ONLY, dataset_name="golden", write_outputs=False, compare_snapshots=True, fail_on_snapshot_drift=True)
    result = harness.run(req)

    assert result.status == RegressionRunStatus.FAILED
    assert result.snapshot_comparison["status"] == "DRIFT"
