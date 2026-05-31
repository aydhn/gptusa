from typing import Any, Dict, Optional, Tuple, List
from pathlib import Path
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLFoundationIngestionResult,
    create_ml_foundation_ingestion_id,
    MLDatasetAssemblyRiskFlag,
    ml_foundation_ingestion_result_to_dict
)
from datetime import datetime, timezone
import json

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def ingest_ml_foundation_review_payload(payload: Dict[str, Any]) -> MLFoundationIngestionResult:
    result = MLFoundationIngestionResult(
        ingestion_id=create_ml_foundation_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=None,
        available=True,
        final_closure_ingested=True,
        final_closure_artifacts_loaded=True,
        source_registry_built=payload.get("source_registry_built", False),
        feature_contract_built=payload.get("feature_contract_built", False),
        target_contract_built=payload.get("target_contract_built", False),
        label_contract_built=payload.get("label_contract_built", False),
        dataset_contract_built=payload.get("dataset_contract_built", False),
        leakage_guard_built=payload.get("leakage_guard_built", False),
        non_activation_boundary_validated=payload.get("non_activation_boundary_validated", False),
        governance_built=payload.get("governance_built", False),
        readiness_gate_built=payload.get("readiness_gate_built", False),
        readiness_gate_passed=payload.get("readiness_gate_passed", False),
        ready_for_phase137=payload.get("ready_for_phase137", False),
        metadata_only=payload.get("metadata_only", True),
        research_data_only=payload.get("research_data_only", True),
        activation_allowed=payload.get("activation_allowed", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        deployment_allowed=payload.get("deployment_allowed", False),
        active_paper_enabled=payload.get("active_paper_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        order_creation_enabled=payload.get("order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        scraping_enabled=payload.get("scraping_enabled", False),
        html_parse_enabled=payload.get("html_parse_enabled", False),
        paid_api_enabled=payload.get("paid_api_enabled", False),
        dashboard_enabled=payload.get("dashboard_enabled", False),
        network_default_enabled=payload.get("network_default_enabled", False),
        daemon_started=payload.get("daemon_started", False),
        scheduler_enabled=payload.get("scheduler_enabled", False),
        training_started=payload.get("training_started", False),
        prediction_started=payload.get("prediction_started", False),
        model_training_used=payload.get("model_training_used", False),
        model_prediction_used=payload.get("model_prediction_used", False),
        heavy_ml_dependency_used=payload.get("heavy_ml_dependency_used", False),
        produces_trade_signal=payload.get("produces_trade_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        investment_advice=payload.get("investment_advice", False),
        network_used=payload.get("network_used", False),
        paid_api_used=payload.get("paid_api_used", False),
        scraping_used=payload.get("scraping_used", False),
        html_parsing_used=payload.get("html_parsing_used", False),
        broker_used=payload.get("broker_used", False),
        order_created=payload.get("order_created", False),
        paper_state_mutated=payload.get("paper_state_mutated", False),
        telegram_real_sent=payload.get("telegram_real_sent", False),
        dashboard_started=payload.get("dashboard_started", False),
        valid_for_phase137=True
    )
    if not payload:
        result.valid_for_phase137 = False
        result.risk_flags.append(MLDatasetAssemblyRiskFlag.ML_FOUNDATION_REVIEW_MISSING)
    if not result.ready_for_phase137:
        result.valid_for_phase137 = False
        result.risk_flags.append(MLDatasetAssemblyRiskFlag.PHASE136_NOT_READY)
    return result

def ingest_latest_ml_foundation_review_from_store(data_root: Path) -> MLFoundationIngestionResult:
    review_dir = data_root / "ml_research" / "foundation" / "reviews"
    if not review_dir.exists():
        res = ingest_ml_foundation_review_payload({})
        res.available = False
        return res
    files = list(review_dir.glob("*.json"))
    if not files:
        res = ingest_ml_foundation_review_payload({})
        res.available = False
        return res
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest_file = files[0]
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        res = ingest_ml_foundation_review_payload(payload)
        res.source_path = str(latest_file)
        return res
    except Exception as e:
        res = ingest_ml_foundation_review_payload({})
        res.available = False
        res.errors.append(f"Failed to load foundation review: {str(e)}")
        return res

def extract_ml_foundation_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_ml_source_registry(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("source_registry")

def extract_ml_dataset_contract(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("dataset_contract")

def extract_ml_leakage_guard(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("leakage_guard")

def extract_ml_non_activation_boundary(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("non_activation_boundary")

def extract_ml_foundation_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def ml_foundation_supports_phase137(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    if not payload.get("ready_for_phase137", False):
        errors.append("ready_for_phase137 is False")
    return len(errors) == 0, errors

def ml_foundation_ingestion_to_text(result: MLFoundationIngestionResult) -> str:
    return json.dumps(ml_foundation_ingestion_result_to_dict(result), indent=2)
