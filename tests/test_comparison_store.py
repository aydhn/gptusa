import pytest
from pathlib import Path
from usa_signal_bot.comparison.comparison_store import (
    build_comparison_run_dir, write_comparison_result_json, read_comparison_result_json,
    list_comparison_runs, get_latest_comparison_run_dir, comparison_store_summary
)
from usa_signal_bot.comparison.comparison_models import ComparisonRunResult, ComparisonRunRequest
from usa_signal_bot.core.enums import ComparisonReportType, ComparisonStatus, ExecutionRealismBucket, GapSeverity

def test_build_run_dir_safe(tmp_path):
    d = build_comparison_run_dir(tmp_path, "run1")
    assert d.name == "run1"

    from usa_signal_bot.core.exceptions import ComparisonStorageError
    with pytest.raises(ComparisonStorageError):
        build_comparison_run_dir(tmp_path, "../run2")

def test_write_read_result(tmp_path):
    req = ComparisonRunRequest("req1", ComparisonReportType.FULL_COMPARISON, paper_run_id="p1")
    res = ComparisonRunResult(
        run_id="run1", created_at_utc="now", status=ComparisonStatus.EMPTY, request=req,
        paper_source=None, backtest_source=None, scan_source=None, matched_trades=[],
        performance_gap=None, execution_gap=None, signal_drift=None,
        execution_realism_bucket=ExecutionRealismBucket.UNKNOWN,
        overall_gap_severity=GapSeverity.UNKNOWN,
        output_paths={}, warnings=[], errors=[]
    )

    d = build_comparison_run_dir(tmp_path, "run1")
    p = d / "result.json"
    write_comparison_result_json(p, res)

    data = read_comparison_result_json(p)
    assert data["run_id"] == "run1"
    assert data["request"]["request_id"] == "req1"

def test_list_and_summary(tmp_path):
    d1 = build_comparison_run_dir(tmp_path, "run1")
    write_comparison_result_json(d1 / "result.json", ComparisonRunResult("run1", "now", ComparisonStatus.EMPTY, ComparisonRunRequest("req1", ComparisonReportType.FULL_COMPARISON), None, None, None, [], None, None, None, ExecutionRealismBucket.UNKNOWN, GapSeverity.UNKNOWN, {}, [], []))

    runs = list_comparison_runs(tmp_path)
    assert len(runs) == 1
    assert get_latest_comparison_run_dir(tmp_path) == d1

    summary = comparison_store_summary(tmp_path)
    assert summary["total_runs"] == 1
