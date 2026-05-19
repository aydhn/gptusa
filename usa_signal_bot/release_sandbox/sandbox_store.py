import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxActivationPlan, SandboxMountPlan, SandboxRuntimeContext,
    SandboxPreviewRun, SandboxValidationResult, ReleaseSandboxReview,
    sandbox_activation_plan_to_dict, sandbox_mount_plan_to_dict,
    sandbox_runtime_context_to_dict, sandbox_preview_run_to_dict,
    sandbox_validation_result_to_dict, release_sandbox_review_to_dict
)

def sandbox_store_dir(data_root: Path) -> Path: return data_root / "release_sandbox"
def sandbox_activation_plans_dir(data_root: Path) -> Path: return sandbox_store_dir(data_root) / "activation_plans"
def sandbox_mount_plans_dir(data_root: Path) -> Path: return sandbox_store_dir(data_root) / "mount_plans"
def sandbox_contexts_dir(data_root: Path) -> Path: return sandbox_store_dir(data_root) / "contexts"
def sandbox_preview_runs_dir(data_root: Path) -> Path: return sandbox_store_dir(data_root) / "preview_runs"
def sandbox_validation_results_dir(data_root: Path) -> Path: return sandbox_store_dir(data_root) / "validation_results"
def sandbox_reviews_dir(data_root: Path) -> Path: return sandbox_store_dir(data_root) / "reviews"

def _write_json(path: Path, data: Dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    return path

def write_sandbox_activation_plan_json(path: Path, item: SandboxActivationPlan) -> Path:
    return _write_json(path, sandbox_activation_plan_to_dict(item))

def write_sandbox_mount_plan_json(path: Path, item: SandboxMountPlan) -> Path:
    return _write_json(path, sandbox_mount_plan_to_dict(item))

def write_sandbox_runtime_context_json(path: Path, item: SandboxRuntimeContext) -> Path:
    return _write_json(path, sandbox_runtime_context_to_dict(item))

def write_sandbox_preview_run_json(path: Path, item: SandboxPreviewRun) -> Path:
    return _write_json(path, sandbox_preview_run_to_dict(item))

def write_sandbox_validation_result_json(path: Path, item: SandboxValidationResult) -> Path:
    return _write_json(path, sandbox_validation_result_to_dict(item))

def write_release_sandbox_review_json(path: Path, item: ReleaseSandboxReview) -> Path:
    return _write_json(path, release_sandbox_review_to_dict(item))

def read_release_sandbox_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    return json.loads(path.read_text())

def list_release_sandbox_reviews(data_root: Path) -> List[Path]:
    d = sandbox_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_release_sandbox_review(data_root: Path) -> Optional[Path]:
    files = list_release_sandbox_reviews(data_root)
    if not files: return None
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]

def sandbox_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_release_sandbox_reviews(data_root))
    }
