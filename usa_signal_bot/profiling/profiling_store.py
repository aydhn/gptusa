import json
from pathlib import Path
from typing import Any

from usa_signal_bot.profiling.profiling_models import (
    ResourceProfile,
    BudgetCalibrationResult,
    ThrottlingPlan,
    ProfilingReviewResult,
    resource_profile_to_dict,
    budget_calibration_result_to_dict,
    throttling_plan_to_dict,
    profiling_review_result_to_dict
)

def profiling_store_dir(data_root: Path) -> Path:
    return data_root / "profiling"

def resource_profiles_dir(data_root: Path) -> Path:
    return profiling_store_dir(data_root) / "profiles"

def calibration_dir(data_root: Path) -> Path:
    return profiling_store_dir(data_root) / "calibration"

def throttling_dir(data_root: Path) -> Path:
    return profiling_store_dir(data_root) / "throttling"

def profiling_reviews_dir(data_root: Path) -> Path:
    return profiling_store_dir(data_root) / "reviews"

def profiling_audit_dir(data_root: Path) -> Path:
    return profiling_store_dir(data_root) / "audit"

def write_resource_profile_json(path: Path, profile: ResourceProfile) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(resource_profile_to_dict(profile), f, indent=2)
    return path

def write_resource_profiles_jsonl(path: Path, profiles: list[ResourceProfile]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        for p in profiles:
            f.write(json.dumps(resource_profile_to_dict(p)) + '\n')
    return path

def write_budget_calibration_result_json(path: Path, result: BudgetCalibrationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(budget_calibration_result_to_dict(result), f, indent=2)
    return path

def write_throttling_plan_json(path: Path, plan: ThrottlingPlan) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(throttling_plan_to_dict(plan), f, indent=2)
    return path

def write_profiling_review_result_json(path: Path, result: ProfilingReviewResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(profiling_review_result_to_dict(result), f, indent=2)
    return path

def read_resource_profile_json(path: Path) -> dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_throttling_plan_json(path: Path) -> dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_resource_profiles(data_root: Path) -> list[Path]:
    p_dir = resource_profiles_dir(data_root)
    if not p_dir.exists():
        return []
    return sorted(list(p_dir.glob("res_profile_*.json")))

def list_calibration_results(data_root: Path) -> list[Path]:
    c_dir = calibration_dir(data_root)
    if not c_dir.exists():
        return []
    return sorted(list(c_dir.glob("calibration_*.json")))

def list_throttling_plans(data_root: Path) -> list[Path]:
    t_dir = throttling_dir(data_root)
    if not t_dir.exists():
        return []
    return sorted(list(t_dir.glob("throttle_plan_*.json")))

def get_latest_resource_profile(data_root: Path) -> Path | None:
    files = list_resource_profiles(data_root)
    return files[-1] if files else None

def get_latest_calibration_result(data_root: Path) -> Path | None:
    files = list_calibration_results(data_root)
    return files[-1] if files else None

def get_latest_throttling_plan(data_root: Path) -> Path | None:
    files = list_throttling_plans(data_root)
    return files[-1] if files else None

def profiling_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "profile_count": len(list_resource_profiles(data_root)),
        "calibration_count": len(list_calibration_results(data_root)),
        "throttling_plan_count": len(list_throttling_plans(data_root))
    }
