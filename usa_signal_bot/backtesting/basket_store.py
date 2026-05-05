import json
import os
from pathlib import Path
from typing import Any

from usa_signal_bot.backtesting.basket_models import (
    BasketSimulationResult, BasketReplayData, BasketExposureSnapshot,
    basket_simulation_result_to_dict, basket_replay_data_to_dict, basket_exposure_snapshot_to_dict
)
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.backtesting.basket_metrics import BasketMetrics, basket_metrics_to_dict
from usa_signal_bot.backtesting.allocation_drift import AllocationDriftReport, allocation_drift_report_to_text
from usa_signal_bot.backtesting.basket_validation import BasketValidationReport
from usa_signal_bot.core.exceptions import BasketStorageError

def basket_store_dir(data_root: Path) -> Path:
    d = data_root / "backtests" / "baskets"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_basket_run_dir(data_root: Path, run_id: str) -> Path:
    if ".." in run_id or "/" in run_id or "\\" in run_id:
        raise BasketStorageError("Invalid run_id for path generation")
    d = basket_store_dir(data_root) / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_basket_simulation_result_json(path: Path, result: BasketSimulationResult) -> Path:
    try:
        data = basket_simulation_result_to_dict(result)
        # Avoid writing massive lists to result.json, they belong in jsonl files
        if "basket_exposure_snapshots" in data:
            data["basket_exposure_snapshots"] = []
        if "order_intents" in data:
            data["order_intents"] = []
        if "fills" in data:
            data["fills"] = []

        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write result json: {e}")

def write_basket_replay_data_json(path: Path, data: BasketReplayData) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(basket_replay_data_to_dict(data), f, indent=2)
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write replay data json: {e}")

def write_basket_exposure_snapshots_jsonl(path: Path, snapshots: list[BasketExposureSnapshot]) -> Path:
    try:
        with open(path, "w") as f:
            for snap in snapshots:
                f.write(json.dumps(basket_exposure_snapshot_to_dict(snap)) + "\n")
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write exposure snapshots jsonl: {e}")

def write_basket_orders_jsonl(path: Path, orders: list[BacktestOrderIntent]) -> Path:
    try:
        from dataclasses import asdict
        with open(path, "w") as f:
            for order in orders:
                f.write(json.dumps(asdict(order)) + "\n")
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write orders jsonl: {e}")

def write_basket_fills_jsonl(path: Path, fills: list[BacktestFill]) -> Path:
    try:
        from dataclasses import asdict
        with open(path, "w") as f:
            for fill in fills:
                f.write(json.dumps(asdict(fill)) + "\n")
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write fills jsonl: {e}")

def write_basket_metrics_json(path: Path, metrics: BasketMetrics) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(basket_metrics_to_dict(metrics), f, indent=2)
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write metrics json: {e}")

def write_allocation_drift_report_json(path: Path, report: AllocationDriftReport) -> Path:
    try:
        with open(path, "w") as f:
            json.dump({}, f, indent=2) # Dummy serialization for the mock report
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write drift report json: {e}")

def write_basket_validation_report_json(path: Path, report: BasketValidationReport) -> Path:
    try:
        from dataclasses import asdict
        with open(path, "w") as f:
            json.dump(asdict(report), f, indent=2)
        return path
    except Exception as e:
        raise BasketStorageError(f"Failed to write validation report json: {e}")

def read_basket_simulation_result_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise BasketStorageError(f"File not found: {path}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise BasketStorageError(f"Failed to read result json: {e}")

def list_basket_runs(data_root: Path) -> list[Path]:
    d = basket_store_dir(data_root)
    runs = []
    for p in d.iterdir():
        if p.is_dir() and (p / "result.json").exists():
            runs.append(p)
    runs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return runs

def get_latest_basket_run_dir(data_root: Path) -> Path | None:
    runs = list_basket_runs(data_root)
    return runs[0] if runs else None

def basket_store_summary(data_root: Path) -> dict[str, Any]:
    runs = list_basket_runs(data_root)
    return {
        "run_count": len(runs),
        "latest_run": runs[0].name if runs else None,
        "store_path": str(basket_store_dir(data_root))
    }
