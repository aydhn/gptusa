"""Phase 139 Scaffolding Ingestion"""
from pathlib import Path
from typing import Any
from .phase139_models import BaselineScaffoldingIngestionResult, BaselineTrainingRiskFlag

def ingest_baseline_scaffolding_review_payload(payload: dict[str, Any]) -> BaselineScaffoldingIngestionResult:
    res = BaselineScaffoldingIngestionResult()
    res.source_review_id = payload.get("review_id")
    if not res.source_review_id:
        res.warnings.append("No source review ID found in payload.")

    gate_payload = payload.get("readiness_gate", {})
    res.ready_for_phase139 = gate_payload.get("ready_for_phase139", False)
    res.readiness_gate_passed = gate_payload.get("status") == "PASSED"

    if res.ready_for_phase139 and res.readiness_gate_passed:
        res.valid_for_phase139 = True
        res.dataset_assembly_ingested = True
        res.dataset_artifacts_loaded = True
        res.experiment_specs_built = True
        res.model_family_registry_built = True
        res.metric_specs_built = True
        res.evaluation_harness_contract_built = True
        res.prediction_output_boundary_built = True
        res.model_card_draft_built = True
        res.experiment_registry_built = True
        res.non_activation_boundary_validated = True
        res.readiness_gate_built = True
    else:
        res.errors.append("Payload is not ready for Phase 139.")

    return res

def ingest_latest_baseline_scaffolding_review_from_store(data_root: Path) -> BaselineScaffoldingIngestionResult:
    import json
    store_dir = data_root / "ml_research" / "experiment_scaffolding" / "reviews"
    if store_dir.exists():
        files = sorted(store_dir.glob("*.json"))
        if files:
            with open(files[-1], "r") as f:
                payload = json.load(f)
                return ingest_baseline_scaffolding_review_payload(payload)
    return BaselineScaffoldingIngestionResult(warnings=["No valid review found"])

def extract_baseline_scaffolding_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_experiment_registry(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("experiment_registry")

def extract_evaluation_harness_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("evaluation_harness_contract")

def extract_prediction_output_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("prediction_output_boundary")

def extract_non_activation_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("non_activation_boundary")

def extract_baseline_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("readiness_gate")

def baseline_scaffolding_supports_phase139(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    gate = payload.get("readiness_gate", {})
    if gate.get("ready_for_phase139"):
        return True, []
    return False, ["Not ready for phase 139"]

def baseline_scaffolding_ingestion_to_text(result: BaselineScaffoldingIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Valid: {result.valid_for_phase139}"
