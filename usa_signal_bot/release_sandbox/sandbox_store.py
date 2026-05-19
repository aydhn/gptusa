import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.exceptions import ReleaseSandboxStorageError
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxActivationPlan, SandboxMountPlan, SandboxRuntimeContext,
    SandboxPreviewRun, SandboxValidationResult, ReleaseSandboxReview,
    sandbox_activation_plan_to_dict, sandbox_mount_plan_to_dict,
    sandbox_runtime_context_to_dict, sandbox_preview_run_to_dict,
    sandbox_validation_result_to_dict, release_sandbox_review_to_dict
)

def sandbox_store_dir(data_root: Path) -> Path:
    d = data_root / "release_sandbox"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_activation_plans_dir(data_root: Path) -> Path:
    d = sandbox_store_dir(data_root) / "activation_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_mount_plans_dir(data_root: Path) -> Path:
    d = sandbox_store_dir(data_root) / "mount_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_contexts_dir(data_root: Path) -> Path:
    d = sandbox_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_preview_runs_dir(data_root: Path) -> Path:
    d = sandbox_store_dir(data_root) / "preview_runs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_validation_results_dir(data_root: Path) -> Path:
    d = sandbox_store_dir(data_root) / "validation_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_reviews_dir(data_root: Path) -> Path:
    d = sandbox_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_sandbox_activation_plan_json(path: Path, item: SandboxActivationPlan) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sandbox_activation_plan_to_dict(item), f, indent=2)
    return path

def write_sandbox_mount_plan_json(path: Path, item: SandboxMountPlan) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sandbox_mount_plan_to_dict(item), f, indent=2)
    return path

def write_sandbox_runtime_context_json(path: Path, item: SandboxRuntimeContext) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sandbox_runtime_context_to_dict(item), f, indent=2)
    return path

def write_sandbox_preview_run_json(path: Path, item: SandboxPreviewRun) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sandbox_preview_run_to_dict(item), f, indent=2)
    return path

def write_sandbox_validation_result_json(path: Path, item: SandboxValidationResult) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sandbox_validation_result_to_dict(item), f, indent=2)
    return path

def write_release_sandbox_review_json(path: Path, item: ReleaseSandboxReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(release_sandbox_review_to_dict(item), f, indent=2)
    return path

def read_release_sandbox_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ReleaseSandboxStorageError(f"Review file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_release_sandbox_reviews(data_root: Path) -> List[Path]:
    d = sandbox_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), reverse=True)

def get_latest_release_sandbox_review(data_root: Path) -> Optional[Path]:
    files = list_release_sandbox_reviews(data_root)
    if not files:
        return None
    return files[0]

def sandbox_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_release_sandbox_reviews(data_root))
    }
