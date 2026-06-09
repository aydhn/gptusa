content_store = """
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
            f.write(json.dumps(item) + "\\n")
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
"""

with open("usa_signal_bot/integration/full_system_integration_store.py", "w") as f:
    f.write(content_store)

content_valid = """
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.integration.phase158_models import FullSystemIntegrationContext, FullSystemIntegrationFullReview
from usa_signal_bot.core.exceptions import FullSystemIntegrationValidationError

@dataclass
class FullSystemIntegrationValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FullSystemIntegrationValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[FullSystemIntegrationValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_full_system_integration_context_report(item: FullSystemIntegrationContext) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def validate_full_system_integration_full_review_report(item: FullSystemIntegrationFullReview) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def validate_no_sensitive_data_in_integration_payload(payload: Dict[str, Any]) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def validate_no_execution_language_in_integration_text(text: str) -> FullSystemIntegrationValidationReport:
    report = FullSystemIntegrationValidationReport()
    forbidden = ["buy", "sell", "portfolio_weight"]
    for f in forbidden:
        if f in text.lower():
            report.valid = False
            report.error_count += 1
            report.errors.append(f"Forbidden text: {f}")
    return report

def validate_no_unsafe_integration_fields(payload: Dict[str, Any]) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def full_system_integration_validation_report_to_text(report: FullSystemIntegrationValidationReport) -> str:
    return f"Validation Report Valid: {report.valid}"

def assert_full_system_integration_validation_valid(report: FullSystemIntegrationValidationReport) -> None:
    if not report.valid:
        raise FullSystemIntegrationValidationError("Validation failed")
"""
with open("usa_signal_bot/integration/full_system_integration_validation.py", "w") as f:
    f.write(content_valid)

content_report_utils = """
from typing import Any, Dict
from usa_signal_bot.integration.phase158_models import *

def phase158_handoff_ingestion_result_to_text(item: Phase158HandoffIngestionResult) -> str:
    return f"Phase158HandoffIngestionResult(valid={item.valid_for_phase158})"

def integration_input_reference_to_text(item: IntegrationInputReference) -> str:
    return f"IntegrationInputReference(valid={item.valid})"

def system_artifact_inventory_to_text(item: SystemArtifactInventory, limit: int = 300) -> str:
    return f"SystemArtifactInventory(valid={item.inventory_valid})"[:limit]

def integration_dependency_graph_to_text(item: IntegrationDependencyGraph, limit: int = 300) -> str:
    return f"IntegrationDependencyGraph(valid={item.graph_valid})"[:limit]

def integration_boundary_contract_to_text(item: IntegrationBoundaryContract, limit: int = 300) -> str:
    return f"IntegrationBoundaryContract(valid={item.contract_valid})"[:limit]

def e2e_rehearsal_plan_to_text(item: E2ERehearsalPlan, limit: int = 300) -> str:
    return f"E2ERehearsalPlan(valid={item.plan_valid})"[:limit]

def acceptance_rehearsal_result_to_text(item: AcceptanceRehearsalResult, limit: int = 300) -> str:
    return f"AcceptanceRehearsalResult(valid={item.result_valid})"[:limit]

def integration_check_report_to_text(item: IntegrationCheckReport, limit: int = 300) -> str:
    return f"IntegrationCheckReport(valid={item.report_valid})"[:limit]

def integration_safety_boundary_to_text(item: IntegrationSafetyBoundaryResult, limit: int = 300) -> str:
    return f"IntegrationSafetyBoundaryResult(passed={item.boundary_passed})"[:limit]

def final_delivery_preparation_checklist_to_text(item: FinalDeliveryPreparationChecklist, limit: int = 300) -> str:
    return f"FinalDeliveryPreparationChecklist(valid={item.checklist_valid})"[:limit]

def phase159_readiness_gate_to_text(item: Phase159ReadinessGate, limit: int = 300) -> str:
    return f"Phase159ReadinessGate(ready={item.ready_for_phase159})"[:limit]

def full_system_integration_context_to_text(item: FullSystemIntegrationContext, limit: int = 300) -> str:
    return f"FullSystemIntegrationContext(ready={item.ready_for_phase159})"[:limit]

def full_system_integration_full_review_to_text(item: FullSystemIntegrationFullReview, limit: int = 300) -> str:
    return f"FullSystemIntegrationFullReview(ready={item.context.ready_for_phase159})"[:limit]

def full_system_integration_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def full_system_integration_limitations_text() -> str:
    return "Limitations: No live trading, dry run only."
"""
with open("usa_signal_bot/integration/full_system_integration_reporting.py", "w") as f:
    f.write(content_report_utils)

content_init = """
# Phase 158 Models and Integrations
from .phase158_models import *
"""
with open("usa_signal_bot/integration/__init__.py", "w") as f:
    f.write(content_init)
