import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from usa_signal_bot.scheduler.scheduler_models import (
    SchedulerPlan, SchedulerRunResult, LockAcquisitionResult, ConcurrencyDecisionResult,
    scheduler_plan_to_dict, scheduler_run_result_to_dict, lock_acquisition_result_to_dict, concurrency_decision_result_to_dict
)
from usa_signal_bot.scheduler.atomic_io import atomic_write_json

def scheduler_store_dir(data_root: Path) -> Path:
    d = data_root / "scheduler"
    d.mkdir(parents=True, exist_ok=True)
    return d

def locks_dir(data_root: Path) -> Path:
    d = scheduler_store_dir(data_root) / "locks"
    d.mkdir(parents=True, exist_ok=True)
    return d

def scheduler_plans_dir(data_root: Path) -> Path:
    d = scheduler_store_dir(data_root) / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def scheduler_runs_dir(data_root: Path) -> Path:
    d = scheduler_store_dir(data_root) / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def scheduler_audit_dir(data_root: Path) -> Path:
    d = scheduler_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def idempotency_store_path(data_root: Path) -> Path:
    return scheduler_store_dir(data_root) / "idempotency.jsonl"

def write_scheduler_plan_json(path: Path, plan: SchedulerPlan) -> Path:
    atomic_write_json(path, scheduler_plan_to_dict(plan))
    return path

def write_scheduler_run_result_json(path: Path, result: SchedulerRunResult) -> Path:
    atomic_write_json(path, scheduler_run_result_to_dict(result))
    return path

def write_lock_acquisition_result_json(path: Path, result: LockAcquisitionResult) -> Path:
    atomic_write_json(path, lock_acquisition_result_to_dict(result))
    return path

def write_stale_lock_report_json(path: Path, report: Any) -> Path:
    from usa_signal_bot.scheduler.stale_lock_detector import stale_lock_report_to_dict
    atomic_write_json(path, stale_lock_report_to_dict(report))
    return path

def write_concurrency_decision_json(path: Path, result: ConcurrencyDecisionResult) -> Path:
    atomic_write_json(path, concurrency_decision_result_to_dict(result))
    return path

def read_scheduler_plan_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def read_scheduler_run_result_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def list_scheduler_plans(data_root: Path) -> List[Path]:
    d = scheduler_plans_dir(data_root)
    return sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

def list_scheduler_runs(data_root: Path) -> List[Path]:
    d = scheduler_runs_dir(data_root)
    return sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

def list_lock_files(data_root: Path) -> List[Path]:
    d = locks_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_scheduler_plan(data_root: Path) -> Optional[Path]:
    files = list_scheduler_plans(data_root)
    return files[0] if files else None

def get_latest_scheduler_run(data_root: Path) -> Optional[Path]:
    files = list_scheduler_runs(data_root)
    return files[0] if files else None

def scheduler_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "plans_count": len(list_scheduler_plans(data_root)),
        "runs_count": len(list_scheduler_runs(data_root)),
        "locks_count": len(list_lock_files(data_root))
    }
