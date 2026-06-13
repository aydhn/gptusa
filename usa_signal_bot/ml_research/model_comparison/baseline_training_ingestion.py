from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any, Tuple, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    BaselineTrainingIngestionResult,
    create_baseline_training_ingestion_id
)

def _extract_ingestion_flags(payload: dict[str, Any]) -> dict[str, bool]:
    ingestion = payload.get("ingestion", {})
    return {
        "scaffolding_ingested": ingestion.get("scaffolding_ingested", False),
        "dataset_loaded": ingestion.get("dataset_loaded", False),
        "scaffolding_artifacts_loaded": ingestion.get("scaffolding_artifacts_loaded", False)
    }

def _extract_context_flags(payload: dict[str, Any]) -> dict[str, bool]:
    context = payload.get("context", {})
    return {
        "training_jobs_built": context.get("training_jobs_built", False),
        "baseline_models_trained": context.get("baseline_models_trained", False),
        "offline_predictions_built": context.get("offline_predictions_built", False),
        "evaluation_metrics_built": context.get("evaluation_metrics_built", False),
        "evaluation_report_built": context.get("evaluation_report_built", False),
        "model_registry_built": context.get("model_registry_built", False),
        "model_cards_updated": context.get("model_cards_updated", False),
        "training_boundary_validated": context.get("training_boundary_validated", False)
    }

def _extract_readiness_flags(payload: dict[str, Any]) -> dict[str, Any]:
    readiness_gate = payload.get("readiness_gate", {})
    return {
        "ready_for_phase140": readiness_gate.get("ready_for_phase140", False),
        "readiness_gate_passed": readiness_gate.get("status") == "PASSED",
        "research_data_only": readiness_gate.get("research_data_only", False),
        "offline_ml_research_only": readiness_gate.get("offline_ml_research_only", False),
        "activation_allowed": readiness_gate.get("activation_allowed", True),
        "heavy_ml_dependency_used": readiness_gate.get("heavy_ml_dependency_used", True)
    }

def _build_safety_flags() -> dict[str, bool]:
    return {
        "activation_allowed": False,
        "strategy_activation_allowed": False,
        "deployment_allowed": False,
        "active_paper_enabled": False,
        "broker_execution_enabled": False,
        "order_creation_enabled": False,
        "paper_state_mutation_enabled": False,
        "telegram_real_send_enabled": False,
        "scraping_enabled": False,
        "html_parse_enabled": False,
        "paid_api_enabled": False,
        "dashboard_enabled": False,
        "network_default_enabled": False,
        "daemon_started": False,
        "scheduler_enabled": False,
        "local_offline_training_used": True,
        "offline_evaluation_prediction_used": True,
        "live_inference_enabled": False,
        "online_inference_enabled": False,
        "heavy_ml_dependency_used": False,
        "produces_trade_signal": False,
        "produces_order_decision": False,
        "produces_portfolio_weights": False,
        "investment_advice": False,
        "network_used": False,
        "paid_api_used": False,
        "scraping_used": False,
        "html_parsing_used": False,
        "broker_used": False,
        "order_created": False,
        "paper_state_mutated": False,
        "telegram_real_sent": False,
        "dashboard_started": False,
    }

def _validate_payload(readiness_flags: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    valid_for_phase140 = True

    if not readiness_flags.get("ready_for_phase140"):
        errors.append("Payload is not marked ready_for_phase140")
        valid_for_phase140 = False

    if readiness_flags.get("activation_allowed") or readiness_flags.get("heavy_ml_dependency_used"):
        errors.append("Payload indicates execution/deployment risks")
        valid_for_phase140 = False

    return valid_for_phase140, errors

def ingest_baseline_training_review_payload(payload: dict[str, Any]) -> BaselineTrainingIngestionResult:
    # A dummy logic to represent checking fields from a phase139 review payload
    source_review_id = payload.get("review_id")

    ingestion_flags = _extract_ingestion_flags(payload)
    context_flags = _extract_context_flags(payload)
    readiness_flags = _extract_readiness_flags(payload)
    safety_flags = _build_safety_flags()

    valid_for_phase140, errors = _validate_payload(readiness_flags)

    kwargs = {
        "ingestion_id": create_baseline_training_ingestion_id(),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_path": None,
        "source_review_id": source_review_id,
        "source_context_id": None,
        "available": True,
        **ingestion_flags,
        **context_flags,
        "readiness_gate_built": True,
        "readiness_gate_passed": readiness_flags["readiness_gate_passed"],
        "ready_for_phase140": readiness_flags["ready_for_phase140"],
        "metadata_only": True,
        "research_data_only": readiness_flags["research_data_only"],
        "offline_ml_research_only": readiness_flags["offline_ml_research_only"],
        **safety_flags,
        "valid_for_phase140": valid_for_phase140,
        "risk_flags": [],
        "warnings": [],
        "errors": errors,
        "metadata": {}
    }

    return BaselineTrainingIngestionResult(**kwargs)

def ingest_latest_baseline_training_review_from_store(data_root: Path) -> BaselineTrainingIngestionResult:
    # A dummy logic
    raise NotImplementedError()

def extract_baseline_training_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_non_activation_model_registry(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("model_registry")

def extract_offline_evaluation_reports(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("evaluation_reports", [])

def extract_offline_prediction_artifacts(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("prediction_artifacts", [])

def extract_fitted_model_artifacts(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("fitted_model_artifacts", [])

def extract_baseline_training_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("readiness_gate")

def baseline_training_supports_phase140(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    valid = payload.get("readiness_gate", {}).get("ready_for_phase140", False)
    errors = []
    if not valid:
        errors.append("Not ready for phase 140")
    return valid, errors

def baseline_training_ingestion_to_text(result: BaselineTrainingIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id}, Valid: {result.valid_for_phase140}"
