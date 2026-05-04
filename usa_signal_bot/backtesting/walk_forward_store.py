import json
import os
from pathlib import Path
from typing import Any
from usa_signal_bot.core.exceptions import WalkForwardStorageError
from usa_signal_bot.backtesting.walk_forward_models import (
    WalkForwardRunResult,
    WalkForwardWindow,
    WalkForwardWindowResult,
    walk_forward_run_result_to_dict,
    walk_forward_window_to_dict,
    walk_forward_window_result_to_dict
)
from usa_signal_bot.backtesting.walk_forward_metrics import WalkForwardAggregateMetrics, walk_forward_aggregate_metrics_to_dict
from usa_signal_bot.backtesting.walk_forward_validation import WalkForwardValidationReport
import shutil

def walk_forward_store_dir(data_root: Path) -> Path:
    d = data_root / "backtests" / "walk_forward"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_walk_forward_run_dir(data_root: Path, run_id: str) -> Path:
    if ".." in run_id or "/" in run_id or "\\" in run_id:
        raise WalkForwardStorageError("Invalid run_id for path creation")
    d = walk_forward_store_dir(data_root) / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def _atomic_write_json(path: Path, data: Any) -> Path:
    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    os.replace(temp_path, path)
    return path

def _atomic_write_jsonl(path: Path, data_list: list[Any]) -> Path:
    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        for item in data_list:
            f.write(json.dumps(item, default=str) + "\n")
    os.replace(temp_path, path)
    return path

def write_walk_forward_result_json(path: Path, result: WalkForwardRunResult) -> Path:
    return _atomic_write_json(path, walk_forward_run_result_to_dict(result))

def write_walk_forward_windows_json(path: Path, windows: list[WalkForwardWindow]) -> Path:
    return _atomic_write_json(path, [walk_forward_window_to_dict(w) for w in windows])

def write_walk_forward_window_results_jsonl(path: Path, results: list[WalkForwardWindowResult]) -> Path:
    return _atomic_write_jsonl(path, [walk_forward_window_result_to_dict(r) for r in results])

def write_walk_forward_aggregate_metrics_json(path: Path, metrics: WalkForwardAggregateMetrics) -> Path:
    return _atomic_write_json(path, walk_forward_aggregate_metrics_to_dict(metrics))

def write_walk_forward_validation_report_json(path: Path, report: WalkForwardValidationReport) -> Path:
    data = {
        "valid": report.valid,
        "issue_count": report.issue_count,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
        "warnings": report.warnings,
        "errors": report.errors
    }
    return _atomic_write_json(path, data)

def list_walk_forward_runs(data_root: Path) -> list[Path]:
    store_dir = walk_forward_store_dir(data_root)
    if not store_dir.exists():
        return []

    runs = []
    for d in store_dir.iterdir():
        if d.is_dir() and d.name.startswith("wf_"):
            runs.append(d)

    # Sort by creation time, descending
    runs.sort(key=lambda x: x.stat().st_ctime, reverse=True)
    return runs

def get_latest_walk_forward_run_dir(data_root: Path) -> Path | None:
    runs = list_walk_forward_runs(data_root)
    if not runs:
        return None
    return runs[0]

def walk_forward_store_summary(data_root: Path) -> dict[str, Any]:
    runs = list_walk_forward_runs(data_root)

    total_size = 0
    for run_dir in runs:
        for f in run_dir.rglob("*"):
            if f.is_file():
                total_size += f.stat().st_size

    return {
        "total_runs": len(runs),
        "total_size_bytes": total_size,
        "latest_run": runs[0].name if runs else None
    }
