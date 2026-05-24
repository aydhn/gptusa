import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraph,
    SafeOrchestrationPlan,
    OrchestrationDryRunResult,
    RuntimeServiceGraphFullReview,
    DependencyContract,
    runtime_service_graph_to_dict,
    safe_orchestration_plan_to_dict,
    orchestration_dry_run_result_to_dict,
    runtime_service_graph_full_review_to_dict,
    dependency_contract_to_dict
)
from usa_signal_bot.core.exceptions import ServiceGraphStorageError

def service_graph_store_dir(data_root: Path) -> Path:
    d = data_root / "runtime_service_graph"
    d.mkdir(parents=True, exist_ok=True)
    return d

def service_graphs_dir(data_root: Path) -> Path:
    d = service_graph_store_dir(data_root) / "graphs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def orchestration_plans_dir(data_root: Path) -> Path:
    d = service_graph_store_dir(data_root) / "orchestration_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def orchestration_results_dir(data_root: Path) -> Path:
    d = service_graph_store_dir(data_root) / "orchestration_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def service_graph_reviews_dir(data_root: Path) -> Path:
    d = service_graph_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dependency_contracts_dir(data_root: Path) -> Path:
    d = service_graph_store_dir(data_root) / "dependency_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_runtime_service_graph_json(path: Path, item: RuntimeServiceGraph) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(runtime_service_graph_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise ServiceGraphStorageError(f"Failed to write graph: {e}")

def write_orchestration_plan_json(path: Path, item: SafeOrchestrationPlan) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(safe_orchestration_plan_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise ServiceGraphStorageError(f"Failed to write plan: {e}")

def write_orchestration_dry_run_result_json(path: Path, item: OrchestrationDryRunResult) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(orchestration_dry_run_result_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise ServiceGraphStorageError(f"Failed to write dry run: {e}")

def write_runtime_service_graph_full_review_json(path: Path, item: RuntimeServiceGraphFullReview) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(runtime_service_graph_full_review_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise ServiceGraphStorageError(f"Failed to write full review: {e}")

def write_dependency_contracts_jsonl(path: Path, items: List[DependencyContract]) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(dependency_contract_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise ServiceGraphStorageError(f"Failed to write contracts: {e}")

def read_runtime_service_graph_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ServiceGraphStorageError("File not found")
    with open(path, "r") as f:
        return json.load(f)

def list_runtime_service_graph_reviews(data_root: Path) -> List[Path]:
    d = service_graph_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_runtime_service_graph_review(data_root: Path) -> Optional[Path]:
    files = list_runtime_service_graph_reviews(data_root)
    if not files:
        return None
    return files[-1]

def service_graph_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "graphs": len(list(service_graphs_dir(data_root).glob("*.json"))),
        "reviews": len(list(service_graph_reviews_dir(data_root).glob("*.json")))
    }
