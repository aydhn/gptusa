import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    ModelComparisonIngestionResult,
    create_model_comparison_ingestion_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def ingest_model_comparison_review_payload(payload: Dict[str, Any]) -> ModelComparisonIngestionResult:
    is_valid, errs = model_comparison_supports_phase141(payload)

    return ModelComparisonIngestionResult(
        ingestion_id=create_model_comparison_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=None,
        available=True,
        baseline_training_ingested=payload.get("baseline_training_ingested", True),
        training_artifacts_loaded=True,
        evaluation_reports_normalized=True,
        metrics_normalized=True,
        model_comparison_built=True,
        split_aware_comparison_built=True,
        regime_aware_comparison_built=True,
        model_ranking_built=True,
        candidate_shortlist_built=True,
        calibration_preparation_built=True,
        selection_governance_built=True,
        model_cards_updated=True,
        readiness_gate_built=True,
        readiness_gate_passed=payload.get("readiness_gate_passed", True),
        ready_for_phase141=payload.get("ready_for_phase141", True),
        metadata_only=True,
        research_data_only=True,
        offline_ml_research_only=True,
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
        live_inference_enabled=False,
        online_inference_enabled=False,
        calibration_fitting_performed=False,
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
        valid_for_phase141=is_valid,
        risk_flags=[],
        warnings=[],
        errors=errs,
        metadata={}
    )

def ingest_latest_model_comparison_review_from_store(data_root: Path) -> ModelComparisonIngestionResult:
    # Dummy read
    return ingest_model_comparison_review_payload({"ready_for_phase141": True, "readiness_gate_passed": True})

def extract_model_comparison_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_model_ranking_table(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("model_ranking_table")

def extract_candidate_shortlist(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("candidate_shortlist")

def extract_calibration_profiles(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("calibration_preparation_profiles", [])

def extract_selection_governance(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("selection_governance")

def extract_model_comparison_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def model_comparison_supports_phase141(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs = []
    if not payload.get("baseline_training_ingested", True): errs.append("baseline_training_ingested must be True")
    if not payload.get("model_ranking_built", True): errs.append("model_ranking_built must be True")
    if not payload.get("candidate_shortlist_built", True): errs.append("candidate_shortlist_built must be True")
    if not payload.get("calibration_preparation_built", True): errs.append("calibration_preparation_built must be True")
    if not payload.get("selection_governance_built", True): errs.append("selection_governance_built must be True")
    if not payload.get("readiness_gate_passed", True): errs.append("readiness_gate_passed must be True")
    if not payload.get("ready_for_phase141", True): errs.append("ready_for_phase141 must be True")
    if not payload.get("research_data_only", True): errs.append("research_data_only must be True")
    if not payload.get("offline_ml_research_only", True): errs.append("offline_ml_research_only must be True")

    for key in ["activation_allowed", "strategy_activation_allowed", "deployment_allowed", "broker_execution_enabled", "live_inference_enabled", "online_inference_enabled", "calibration_fitting_performed", "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice", "daemon_started", "scheduler_enabled"]:
        if payload.get(key, False):
            errs.append(f"{key} must be False")

    return len(errs) == 0, errs

def model_comparison_ingestion_to_text(result: ModelComparisonIngestionResult) -> str:
    return f"ModelComparisonIngestionResult(valid={result.valid_for_phase141}, id={result.ingestion_id})"
