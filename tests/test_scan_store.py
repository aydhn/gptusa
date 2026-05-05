import pytest
from pathlib import Path
from usa_signal_bot.runtime.scan_store import (
    runtime_store_dir, scan_store_dir, build_scan_run_dir,
    write_market_scan_result_json, read_market_scan_result_json,
    write_runtime_state_json, write_pipeline_step_results_jsonl,
    write_scan_manifest_json, write_runtime_validation_report_json,
    list_scan_runs, get_latest_scan_run_dir, scan_store_summary
)
from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest, RuntimeState, PipelineStepResult
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus, PipelineStepName, PipelineStepStatus
from usa_signal_bot.runtime.runtime_validation import RuntimeValidationReport, RuntimeValidationIssue

def test_scan_store(tmp_path):
    assert runtime_store_dir(tmp_path).name == "runtime"
    assert scan_store_dir(tmp_path).name == "scans"

    run_dir = build_scan_run_dir(tmp_path, "run1")
    assert run_dir.name == "run1"

    req = MarketScanRequest(run_name="t", mode=RuntimeMode.DRY_RUN, scope=ScanScope.SMALL_TEST_SET)
    res = MarketScanResult(run_id="run1", created_at_utc="", request=req, status=RuntimeRunStatus.COMPLETED)

    p = run_dir / "result.json"
    write_market_scan_result_json(p, res)
    d = read_market_scan_result_json(p)
    assert d["run_id"] == "run1"

    state = RuntimeState(run_id="run1", mode=RuntimeMode.DRY_RUN, status=RuntimeRunStatus.COMPLETED)
    write_runtime_state_json(run_dir / "state.json", state)

    steps = [PipelineStepResult(step_name=PipelineStepName.PREFLIGHT, status=PipelineStepStatus.COMPLETED)]
    write_pipeline_step_results_jsonl(run_dir / "steps.jsonl", steps)

    write_scan_manifest_json(run_dir / "manifest.json", res)

    rep = RuntimeValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, issues=[], warnings=[], errors=[])
    write_runtime_validation_report_json(run_dir / "validation.json", rep)

    runs = list_scan_runs(tmp_path)
    assert len(runs) == 1

    latest = get_latest_scan_run_dir(tmp_path)
    assert latest.name == "run1"

    summ = scan_store_summary(tmp_path)
    assert summ["total_runs"] == 1
