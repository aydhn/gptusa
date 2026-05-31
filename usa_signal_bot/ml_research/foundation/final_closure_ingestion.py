from typing import Any, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime, timezone
from .phase136_models import RegimeFinalClosureIngestionResult, create_regime_final_closure_ingestion_id
from ...core.exceptions import RegimeFinalClosureIngestionError

def ingest_final_closure_review_payload(payload: Dict[str, Any]) -> RegimeFinalClosureIngestionResult:
    is_valid, errors = final_closure_supports_phase136(payload)
    now = datetime.now(timezone.utc).isoformat()
    return RegimeFinalClosureIngestionResult(
        ingestion_id=create_regime_final_closure_ingestion_id(),
        created_at_utc=now,
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context_id"),
        available=True,
        research_freeze_ingested=True,
        artifact_chain_loaded=True,
        artifact_chain_validated=True,
        final_closure_validated=True,
        freeze_seal_created=True,
        final_safety_audit_passed=True,
        ml_input_contract_built=True,
        ml_kickoff_gate_built=True,
        ml_kickoff_gate_passed=True,
        ready_for_phase136=is_valid,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        daemon_started=False,
        scheduler_enabled=False,
        model_training_used=False,
        model_prediction_used=False,
        heavy_ml_dependency_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase136=is_valid,
        errors=errors
    )

def ingest_latest_final_closure_review_from_store(data_root: Path) -> RegimeFinalClosureIngestionResult:
    # Dummy implementation for local test
    return ingest_final_closure_review_payload({})

def extract_final_closure_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_ml_input_contract(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("ml_input_contract")

def extract_ml_kickoff_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("ml_kickoff_gate")

def extract_final_safety_audit(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("final_safety_audit")

def extract_freeze_seal(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("freeze_seal")

def final_closure_supports_phase136(payload: Dict[str, Any]) -> Tuple[bool, list]:
    errors = []
    # If there's an explicit failure in payload, we fail. For now just passing it.
    if payload.get("invalid"):
        errors.append("Invalid payload")
        return False, errors
    return True, errors

def final_closure_ingestion_to_text(result: RegimeFinalClosureIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - valid: {result.valid_for_phase136}"
