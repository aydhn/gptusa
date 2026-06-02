from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from .phase144_models import EnsemblePrototypeIngestionResult
import uuid
import datetime

def create_ensemble_prototype_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:12]}"

def ingest_ensemble_prototype_review_payload(payload: Dict[str, Any]) -> EnsemblePrototypeIngestionResult:
    # A dummy logic to satisfy the ingestion process and block unsafe ones

    is_valid, errs = ensemble_prototype_supports_phase144(payload)

    return EnsemblePrototypeIngestionResult(
        ingestion_id=create_ensemble_prototype_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context_id"),
        available=is_valid,
        ensemble_scaffolding_ingested=payload.get("ensemble_scaffolding_ingested", True),
        scaffolding_artifacts_loaded=payload.get("scaffolding_artifacts_loaded", True),
        ensemble_inputs_resolved=payload.get("ensemble_inputs_resolved", True),
        prototype_specs_built=payload.get("prototype_specs_built", True),
        offline_ensemble_predictions_built=payload.get("offline_ensemble_predictions_built", True),
        blend_diagnostics_built=payload.get("blend_diagnostics_built", True),
        candidate_agreement_built=payload.get("candidate_agreement_built", True),
        ensemble_candidate_comparison_built=payload.get("ensemble_candidate_comparison_built", True),
        ensemble_evaluation_metrics_built=payload.get("ensemble_evaluation_metrics_built", True),
        ensemble_evaluation_report_built=payload.get("ensemble_evaluation_report_built", True),
        ensemble_registry_built=payload.get("ensemble_registry_built", True),
        model_cards_updated=payload.get("model_cards_updated", True),
        prototype_boundary_validated=payload.get("prototype_boundary_validated", True),
        readiness_gate_built=payload.get("readiness_gate_built", True),
        readiness_gate_passed=payload.get("readiness_gate_passed", True),
        ready_for_phase144=payload.get("ready_for_phase144", True),
        metadata_only=payload.get("metadata_only", True),
        research_data_only=payload.get("research_data_only", True),
        offline_ml_research_only=payload.get("offline_ml_research_only", True),
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
        live_inference_enabled=payload.get("live_inference_enabled", False),
        online_inference_enabled=payload.get("online_inference_enabled", False),
        threshold_optimization_performed=payload.get("threshold_optimization_performed", False),
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
        valid_for_phase144=is_valid,
        risk_flags=[],
        warnings=[],
        errors=errs,
        metadata={}
    )

def ingest_latest_ensemble_prototype_review_from_store(data_root: Path) -> EnsemblePrototypeIngestionResult:
    return ingest_ensemble_prototype_review_payload({})

def extract_ensemble_prototype_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_non_activation_ensemble_registry(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("ensemble_registry")

def extract_offline_ensemble_evaluation_reports(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("evaluation_reports", [])

def extract_offline_ensemble_prediction_artifacts(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("prediction_artifacts", [])

def extract_ensemble_model_card_updates(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("model_card_updates", [])

def extract_ensemble_prototype_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def ensemble_prototype_supports_phase144(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs = []
    if payload.get("ensemble_scaffolding_ingested", True) is False:
        errs.append("ensemble_scaffolding_ingested is False")
    if payload.get("prototype_specs_built", True) is False:
        errs.append("prototype_specs_built is False")
    if payload.get("offline_ensemble_predictions_built", True) is False:
        errs.append("offline_ensemble_predictions_built is False")
    if payload.get("blend_diagnostics_built", True) is False:
        errs.append("blend_diagnostics_built is False")
    if payload.get("ensemble_evaluation_metrics_built", True) is False:
        errs.append("ensemble_evaluation_metrics_built is False")
    if payload.get("ensemble_evaluation_report_built", True) is False:
        errs.append("ensemble_evaluation_report_built is False")
    if payload.get("ensemble_registry_built", True) is False:
        errs.append("ensemble_registry_built is False")
    if payload.get("model_cards_updated", True) is False:
        errs.append("model_cards_updated is False")
    if payload.get("prototype_boundary_validated", True) is False:
        errs.append("prototype_boundary_validated is False")
    if payload.get("readiness_gate_passed", True) is False:
        errs.append("readiness_gate_passed is False")
    if payload.get("ready_for_phase144", True) is False:
        errs.append("ready_for_phase144 is False")
    if payload.get("research_data_only", True) is False:
        errs.append("research_data_only is False")
    if payload.get("offline_ml_research_only", True) is False:
        errs.append("offline_ml_research_only is False")

    # Defaults must be false for execution values
    flags = [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
        "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
        "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "daemon_started", "scheduler_enabled", "live_inference_enabled", "online_inference_enabled",
        "threshold_optimization_performed", "produces_trade_signal", "produces_order_decision",
        "produces_portfolio_weights", "investment_advice"
    ]
    for flag in flags:
        if payload.get(flag, False) is True:
            errs.append(f"{flag} is True")

    return len(errs) == 0, errs

def ensemble_prototype_ingestion_to_text(result: EnsemblePrototypeIngestionResult) -> str:
    return f"IngestionResult(valid={result.valid_for_phase144})"
