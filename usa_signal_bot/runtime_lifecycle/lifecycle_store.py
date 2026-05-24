import json
from pathlib import Path
from typing import Any, List, Optional
from usa_signal_bot.core.exceptions import LifecycleStorageError
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    RuntimeLifecycleContext,
    StartupCheckReport,
    ServiceReadinessMatrix,
    ReadinessGate,
    RuntimeLifecycleFullReview,
    runtime_lifecycle_context_to_dict,
    startup_check_report_to_dict,
    service_readiness_matrix_to_dict,
    readiness_gate_to_dict,
    runtime_lifecycle_full_review_to_dict
)

def lifecycle_store_dir(data_root: Path) -> Path:
    d = data_root / "runtime_lifecycle"
    d.mkdir(parents=True, exist_ok=True)
    return d

def lifecycle_contexts_dir(data_root: Path) -> Path:
    d = lifecycle_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def startup_reports_dir(data_root: Path) -> Path:
    d = lifecycle_store_dir(data_root) / "startup_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def readiness_matrices_dir(data_root: Path) -> Path:
    d = lifecycle_store_dir(data_root) / "readiness_matrices"
    d.mkdir(parents=True, exist_ok=True)
    return d

def readiness_gates_dir(data_root: Path) -> Path:
    d = lifecycle_store_dir(data_root) / "readiness_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def lifecycle_reviews_dir(data_root: Path) -> Path:
    d = lifecycle_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, data: dict) -> Path:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
        return path
    except Exception as e:
        raise LifecycleStorageError(f"Failed to write JSON to {path}: {str(e)}")

def write_runtime_lifecycle_context_json(path: Path, item: RuntimeLifecycleContext) -> Path:
    return _write_json(path, runtime_lifecycle_context_to_dict(item))

def write_startup_check_report_json(path: Path, item: StartupCheckReport) -> Path:
    return _write_json(path, startup_check_report_to_dict(item))

def write_service_readiness_matrix_json(path: Path, item: ServiceReadinessMatrix) -> Path:
    return _write_json(path, service_readiness_matrix_to_dict(item))

def write_readiness_gate_json(path: Path, item: ReadinessGate) -> Path:
    return _write_json(path, readiness_gate_to_dict(item))

def write_runtime_lifecycle_full_review_json(path: Path, item: RuntimeLifecycleFullReview) -> Path:
    return _write_json(path, runtime_lifecycle_full_review_to_dict(item))

def read_runtime_lifecycle_full_review_json(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise LifecycleStorageError(f"Failed to read JSON from {path}: {str(e)}")

def list_runtime_lifecycle_reviews(data_root: Path) -> List[Path]:
    d = lifecycle_reviews_dir(data_root)
    return sorted(d.glob("*.json"), reverse=True)

def get_latest_runtime_lifecycle_review(data_root: Path) -> Optional[Path]:
    files = list_runtime_lifecycle_reviews(data_root)
    if files:
        return files[0]
    return None

def lifecycle_store_summary(data_root: Path) -> dict:
    return {
        "contexts_count": len(list(lifecycle_contexts_dir(data_root).glob("*.json"))),
        "startup_reports_count": len(list(startup_reports_dir(data_root).glob("*.json"))),
        "readiness_matrices_count": len(list(readiness_matrices_dir(data_root).glob("*.json"))),
        "readiness_gates_count": len(list(readiness_gates_dir(data_root).glob("*.json"))),
        "reviews_count": len(list_runtime_lifecycle_reviews(data_root)),
        "latest_review_path": str(get_latest_runtime_lifecycle_review(data_root)) if get_latest_runtime_lifecycle_review(data_root) else None
    }
