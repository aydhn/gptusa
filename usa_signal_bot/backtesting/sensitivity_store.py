import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.exceptions import SensitivityStorageError
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterSensitivityRunResult, ParameterGridSpec, ParameterGridCell,
    SensitivityCellResult, parameter_sensitivity_run_result_to_dict,
    parameter_grid_spec_to_dict, parameter_grid_cell_to_dict,
    sensitivity_cell_result_to_dict
)
from usa_signal_bot.backtesting.sensitivity_metrics import SensitivityAggregateMetrics, sensitivity_aggregate_metrics_to_dict
from usa_signal_bot.backtesting.stability_map import StabilityMap, stability_map_to_dict
from usa_signal_bot.backtesting.sensitivity_validation import SensitivityValidationReport

def sensitivity_store_dir(data_root: Path) -> Path:
    d = data_root / "backtests" / "sensitivity"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_sensitivity_run_dir(data_root: Path, run_id: str) -> Path:
    if ".." in run_id or "/" in run_id or "\\" in run_id:
        raise SensitivityStorageError(f"Invalid run_id for path creation: {run_id}")
    d = sensitivity_store_dir(data_root) / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def _atomic_write_json(path: Path, data: Any) -> Path:
    temp_path = path.with_suffix(".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        temp_path.replace(path)
        return path
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise SensitivityStorageError(f"Failed to write json to {path}: {e}")

def write_sensitivity_result_json(path: Path, result: ParameterSensitivityRunResult) -> Path:
    data = parameter_sensitivity_run_result_to_dict(result)
    return _atomic_write_json(path, data)

def write_sensitivity_grid_json(path: Path, grid_spec: ParameterGridSpec, cells: list[ParameterGridCell]) -> Path:
    data = {
        "grid_spec": parameter_grid_spec_to_dict(grid_spec),
        "cells": [parameter_grid_cell_to_dict(c) for c in cells]
    }
    return _atomic_write_json(path, data)

def write_sensitivity_cell_results_jsonl(path: Path, results: list[SensitivityCellResult]) -> Path:
    temp_path = path.with_suffix(".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            for r in results:
                line = json.dumps(sensitivity_cell_result_to_dict(r))
                f.write(line + "\n")
        temp_path.replace(path)
        return path
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise SensitivityStorageError(f"Failed to write jsonl to {path}: {e}")

def write_sensitivity_aggregate_metrics_json(path: Path, metrics: SensitivityAggregateMetrics) -> Path:
    data = sensitivity_aggregate_metrics_to_dict(metrics)
    return _atomic_write_json(path, data)

def write_stability_map_json(path: Path, map_: StabilityMap) -> Path:
    data = stability_map_to_dict(map_)
    return _atomic_write_json(path, data)

def write_sensitivity_validation_report_json(path: Path, report: SensitivityValidationReport) -> Path:
    data = {
        "valid": report.valid,
        "issue_count": report.issue_count,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
        "issues": [{"severity": i.severity, "field": i.field, "message": i.message, "details": i.details} for i in report.issues],
        "warnings": report.warnings,
        "errors": report.errors
    }
    return _atomic_write_json(path, data)

def list_sensitivity_runs(data_root: Path) -> list[Path]:
    d = sensitivity_store_dir(data_root)
    if not d.exists():
        return []
    return [p for p in d.iterdir() if p.is_dir()]

def get_latest_sensitivity_run_dir(data_root: Path) -> Path | None:
    runs = list_sensitivity_runs(data_root)
    if not runs:
        return None
    # Sort by creation time (st_ctime or st_mtime).
    # For simplicity, sorting by dir name is often enough if they contain timestamps, but run_id might not.
    # So we sort by modified time.
    runs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return runs[0]

def sensitivity_store_summary(data_root: Path) -> dict[str, Any]:
    runs = list_sensitivity_runs(data_root)
    return {
        "total_runs": len(runs),
        "run_ids": [p.name for p in runs]
    }
