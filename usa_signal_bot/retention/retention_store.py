import json
from pathlib import Path
from typing import Any
from usa_signal_bot.retention.retention_models import (
    CleanupPlan, CleanupExecutionResult, DiskQuotaReport, RetentionReviewResult, RetentionPolicy,
    cleanup_plan_to_dict, cleanup_execution_result_to_dict, disk_quota_report_to_dict,
    retention_review_result_to_dict, retention_policy_to_dict
)

def retention_store_dir(data_root: Path) -> Path:
    return data_root / "retention"

def cleanup_plans_dir(data_root: Path) -> Path:
    return retention_store_dir(data_root) / "plans"

def cleanup_results_dir(data_root: Path) -> Path:
    return retention_store_dir(data_root) / "results"

def quota_reports_dir(data_root: Path) -> Path:
    return retention_store_dir(data_root) / "quota"

def audit_dir(data_root: Path) -> Path:
    return retention_store_dir(data_root) / "audit"

def _write_json(path: Path, data: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

def write_cleanup_plan_json(path: Path, plan: CleanupPlan) -> Path:
    return _write_json(path, cleanup_plan_to_dict(plan))

def write_cleanup_execution_result_json(path: Path, result: CleanupExecutionResult) -> Path:
    return _write_json(path, cleanup_execution_result_to_dict(result))

def write_disk_quota_report_json(path: Path, report: DiskQuotaReport) -> Path:
    return _write_json(path, disk_quota_report_to_dict(report))

def write_retention_review_result_json(path: Path, result: RetentionReviewResult) -> Path:
    return _write_json(path, retention_review_result_to_dict(result))

def write_retention_policies_json(path: Path, policies: list[RetentionPolicy]) -> Path:
    return _write_json(path, {"policies": [retention_policy_to_dict(p) for p in policies]})

def read_cleanup_plan_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_cleanup_execution_result_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_disk_quota_report_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_cleanup_plans(data_root: Path) -> list[Path]:
    d = cleanup_plans_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")))

def list_cleanup_results(data_root: Path) -> list[Path]:
    d = cleanup_results_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")))

def get_latest_cleanup_plan(data_root: Path) -> Path | None:
    plans = list_cleanup_plans(data_root)
    return plans[-1] if plans else None

def get_latest_cleanup_result(data_root: Path) -> Path | None:
    results = list_cleanup_results(data_root)
    return results[-1] if results else None

def get_latest_quota_report(data_root: Path) -> Path | None:
    d = quota_reports_dir(data_root)
    if not d.exists():
        return None
    reports = sorted(list(d.glob("*.json")))
    return reports[-1] if reports else None

def retention_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "plans_count": len(list_cleanup_plans(data_root)),
        "results_count": len(list_cleanup_results(data_root)),
        "has_audit": (audit_dir(data_root) / "cleanup_audit.jsonl").exists()
    }
