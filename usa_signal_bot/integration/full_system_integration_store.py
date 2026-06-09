
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.integration.phase158_models import (
    FullSystemIntegrationContext, FullSystemIntegrationFullReview, IntegrationInputReference,
    SystemArtifactInventory, IntegrationDependencyGraph, IntegrationBoundaryContract,
    E2ERehearsalPlan, DryRunExecutionStep, AcceptanceRehearsalResult, IntegrationCheckReport,
    IntegrationSafetyBoundaryResult, FinalDeliveryPreparationChecklist, Phase159ReadinessGate
)

def full_system_integration_store_dir(data_root: Path) -> Path:
    d = data_root / "integration" / "phase158"
    d.mkdir(parents=True, exist_ok=True)
    return d

def full_system_integration_contexts_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def full_system_integration_reviews_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def integration_inputs_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "inputs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def artifact_inventories_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "artifact_inventories"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dependency_graphs_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "dependency_graphs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def boundary_contracts_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "boundary_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_plans_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "rehearsal_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_results_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "rehearsal_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def integration_reports_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "integration_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def safety_boundaries_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "safety_boundaries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_delivery_checklists_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "final_delivery_checklists"
    d.mkdir(parents=True, exist_ok=True)
    return d

def phase159_gates_dir(data_root: Path) -> Path:
    d = full_system_integration_store_dir(data_root) / "phase159_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, data: Dict[str, Any]) -> Path:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def _write_jsonl(path: Path, data_list: List[Dict[str, Any]]) -> Path:
    with open(path, "w") as f:
        for item in data_list:
            f.write(json.dumps(item) + "\n")
    return path

def write_full_system_integration_context_json(path: Path, item: FullSystemIntegrationContext) -> Path:
    return _write_json(path, item.to_dict())

def write_full_system_integration_full_review_json(path: Path, item: FullSystemIntegrationFullReview) -> Path:
    return _write_json(path, item.to_dict())

def write_integration_input_refs_jsonl(path: Path, items: List[IntegrationInputReference]) -> Path:
    return _write_jsonl(path, [i.to_dict() for i in items])

def write_system_artifact_inventory_json(path: Path, item: SystemArtifactInventory) -> Path:
    return _write_json(path, item.to_dict())

def write_integration_dependency_graph_json(path: Path, item: IntegrationDependencyGraph) -> Path:
    return _write_json(path, item.to_dict())

def write_integration_boundary_contract_json(path: Path, item: IntegrationBoundaryContract) -> Path:
    return _write_json(path, item.to_dict())

def write_e2e_rehearsal_plan_json(path: Path, item: E2ERehearsalPlan) -> Path:
    return _write_json(path, item.to_dict())

def write_dry_run_execution_steps_jsonl(path: Path, items: List[DryRunExecutionStep]) -> Path:
    return _write_jsonl(path, [i.to_dict() for i in items])

def write_acceptance_rehearsal_result_json(path: Path, item: AcceptanceRehearsalResult) -> Path:
    return _write_json(path, item.to_dict())

def write_integration_reports_jsonl(path: Path, items: List[IntegrationCheckReport]) -> Path:
    return _write_jsonl(path, [i.to_dict() for i in items])

def write_integration_safety_boundary_json(path: Path, item: IntegrationSafetyBoundaryResult) -> Path:
    return _write_json(path, item.to_dict())

def write_final_delivery_preparation_checklist_json(path: Path, item: FinalDeliveryPreparationChecklist) -> Path:
    return _write_json(path, item.to_dict())

def write_phase159_readiness_gate_json(path: Path, item: Phase159ReadinessGate) -> Path:
    return _write_json(path, item.to_dict())

def read_full_system_integration_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_full_system_integration_reviews(data_root: Path) -> List[Path]:
    d = full_system_integration_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_full_system_integration_review(data_root: Path) -> Optional[Path]:
    files = list_full_system_integration_reviews(data_root)
    return files[-1] if files else None

def full_system_integration_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews_count": len(list_full_system_integration_reviews(data_root))}
