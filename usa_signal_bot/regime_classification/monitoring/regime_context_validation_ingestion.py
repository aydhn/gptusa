import json
import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeContextValidationIngestionResult,
    create_regime_context_validation_ingestion_id,
    RegimeMonitoringRiskFlag
)
from usa_signal_bot.core.exceptions import RegimeContextValidationIngestionError

def extract_regime_context_validation_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_compatibility_validation_result(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("compatibility_result")

def extract_conditional_diagnostics(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("conditional_diagnostics", [])

def extract_conditional_diagnostics_profiles(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("diagnostic_profiles", [])

def extract_regime_acceptance_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("acceptance_gate")

def regime_context_validation_supports_phase133(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    gate = extract_regime_acceptance_gate(payload)
    if not gate:
        errors.append("No acceptance gate found")
    elif not gate.get("ready_for_phase133", False):
        errors.append("ready_for_phase133 is false in acceptance gate")

    context = extract_regime_context_validation_context(payload)
    if not context:
        errors.append("No context found")
    else:
        if not context.get("ready_for_phase133", False):
            errors.append("ready_for_phase133 is false in context")
        if context.get("activation_allowed", True):
             errors.append("activation_allowed is true")
        if context.get("produces_trade_signal", True):
             errors.append("produces_trade_signal is true")

    if errors:
        return False, errors
    return True, []

def ingest_regime_context_validation_review_payload(payload: Dict[str, Any]) -> RegimeContextValidationIngestionResult:
    context = extract_regime_context_validation_context(payload)
    if not context:
        raise RegimeContextValidationIngestionError("No context found in payload")

    gate = extract_regime_acceptance_gate(payload)

    valid, errors = regime_context_validation_supports_phase133(payload)

    risk_flags = []
    if not valid:
        risk_flags.append(RegimeMonitoringRiskFlag.CONTEXT_VALIDATION_REVIEW_INVALID)

    return RegimeContextValidationIngestionResult(
        ingestion_id=create_regime_context_validation_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=context.get("context_id"),
        available=True,
        alignment_ingested=context.get("alignment_ingested", False),
        alignment_artifacts_loaded=context.get("alignment_artifacts_loaded", False),
        validation_specs_ready=context.get("validation_specs_ready", False),
        compatibility_validated=context.get("compatibility_validated", False),
        conditional_diagnostics_built=context.get("conditional_diagnostics_built", False),
        acceptance_gate_built=context.get("acceptance_gate_built", False),
        acceptance_gate_passed=context.get("acceptance_gate_passed", False),
        ready_for_phase133=valid,
        metadata_only=context.get("metadata_only", True),
        research_data_only=context.get("research_data_only", True),
        activation_allowed=context.get("activation_allowed", False),
        strategy_activation_allowed=context.get("strategy_activation_allowed", False),
        deployment_allowed=context.get("deployment_allowed", False),
        active_paper_enabled=context.get("active_paper_enabled", False),
        broker_execution_enabled=context.get("broker_execution_enabled", False),
        order_creation_enabled=context.get("order_creation_enabled", False),
        paper_state_mutation_enabled=context.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=context.get("telegram_real_send_enabled", False),
        scraping_enabled=context.get("scraping_enabled", False),
        html_parse_enabled=context.get("html_parse_enabled", False),
        paid_api_enabled=context.get("paid_api_enabled", False),
        dashboard_enabled=context.get("dashboard_enabled", False),
        network_default_enabled=context.get("network_default_enabled", False),
        model_training_used=context.get("model_training_used", False),
        model_prediction_used=context.get("model_prediction_used", False),
        heavy_ml_dependency_used=context.get("heavy_ml_dependency_used", False),
        produces_trade_signal=context.get("produces_trade_signal", False),
        produces_order_decision=context.get("produces_order_decision", False),
        produces_portfolio_weights=context.get("produces_portfolio_weights", False),
        investment_advice=context.get("investment_advice", False),
        network_used=context.get("network_used", False),
        paid_api_used=context.get("paid_api_used", False),
        scraping_used=context.get("scraping_used", False),
        html_parsing_used=context.get("html_parsing_used", False),
        broker_used=context.get("broker_used", False),
        order_created=context.get("order_created", False),
        paper_state_mutated=context.get("paper_state_mutated", False),
        telegram_real_sent=context.get("telegram_real_sent", False),
        dashboard_started=context.get("dashboard_started", False),
        valid_for_phase133=valid,
        risk_flags=risk_flags,
        warnings=errors,
        errors=errors if not valid else [],
        metadata={"ingested_from": "payload"}
    )

def ingest_latest_regime_context_validation_review_from_store(data_root: Path) -> RegimeContextValidationIngestionResult:
    from usa_signal_bot.regime_classification.validation.regime_context_validation_store import get_latest_regime_context_validation_review, read_regime_context_validation_full_review_json
    path = get_latest_regime_context_validation_review(data_root)
    if not path:
        raise RegimeContextValidationIngestionError("No latest context validation review found in store")
    payload = read_regime_context_validation_full_review_json(path)
    res = ingest_regime_context_validation_review_payload(payload)
    res.source_path = str(path)
    res.metadata["ingested_from"] = "store"
    return res

def regime_context_validation_ingestion_to_text(result: RegimeContextValidationIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id}, Valid for Phase 133: {result.valid_for_phase133}, Review ID: {result.source_review_id}"
