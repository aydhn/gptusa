import json
from pathlib import Path
from typing import Any, Optional, Dict, List, Tuple
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsembleScaffoldingIngestionResult,
    create_ensemble_scaffolding_ingestion_id,
    EnsemblePrototypeRiskFlag
)
from usa_signal_bot.core.exceptions import EnsembleScaffoldingIngestionError

def ingest_ensemble_scaffolding_review_payload(payload: Dict[str, Any]) -> EnsembleScaffoldingIngestionResult:
    report_type = payload.get("report_type")

    warnings = []
    errors = []
    risk_flags = []

    if report_type != "ENSEMBLE_SCAFFOLDING_FULL_REVIEW":
        errors.append("Invalid report type. Expected ENSEMBLE_SCAFFOLDING_FULL_REVIEW.")
        risk_flags.append(EnsemblePrototypeRiskFlag.ENSEMBLE_SCAFFOLDING_REVIEW_INVALID)

    context = extract_ensemble_scaffolding_context(payload)
    if not context:
        errors.append("Missing context in ensemble scaffolding review.")
        risk_flags.append(EnsemblePrototypeRiskFlag.ENSEMBLE_SCAFFOLDING_REVIEW_MISSING)
        context = {}

    ready_for_phase143 = context.get("ready_for_phase143", False)
    if not ready_for_phase143:
        errors.append("Ensemble scaffolding is not ready for Phase 143.")
        risk_flags.append(EnsemblePrototypeRiskFlag.PHASE142_NOT_READY)

    # Check safe execution flags
    for flag in ["activation_allowed", "strategy_activation_allowed", "deployment_allowed",
                 "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
                 "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
                 "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
                 "daemon_started", "scheduler_enabled", "live_inference_enabled", "online_inference_enabled",
                 "ensemble_fitting_performed", "final_ensemble_prediction_created",
                 "threshold_optimization_performed", "heavy_ml_dependency_used", "produces_trade_signal",
                 "produces_order_decision", "produces_portfolio_weights", "investment_advice", "network_used",
                 "paid_api_used", "scraping_used", "html_parsing_used", "broker_used", "order_created",
                 "paper_state_mutated", "telegram_real_sent", "dashboard_started"]:
        if context.get(flag, False):
            errors.append(f"Unsafe flag detected: {flag}=True")
            risk_flags.append(EnsemblePrototypeRiskFlag.DEPLOYMENT_RISK) # general mapping

    # Ensure research data only
    if not context.get("research_data_only", False):
         errors.append("research_data_only must be True.")

    if not context.get("offline_ml_research_only", False):
         errors.append("offline_ml_research_only must be True.")

    is_valid = len(errors) == 0

    return EnsembleScaffoldingIngestionResult(
        ingestion_id=create_ensemble_scaffolding_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=context.get("context_id"),
        available=True,
        calibration_diagnostics_ingested=context.get("calibration_diagnostics_ingested", False),
        calibration_artifacts_loaded=context.get("calibration_artifacts_loaded", False),
        ensemble_candidates_resolved=context.get("ensemble_candidates_resolved", False),
        ensemble_family_specs_built=context.get("ensemble_family_specs_built", False),
        candidate_groups_built=context.get("candidate_groups_built", False),
        blend_policy_built=context.get("blend_policy_built", False),
        blend_coefficient_plan_built=context.get("blend_coefficient_plan_built", False),
        prediction_correlation_built=context.get("prediction_correlation_built", False),
        diversity_profiles_built=context.get("diversity_profiles_built", False),
        complementarity_profiles_built=context.get("complementarity_profiles_built", False),
        calibration_aware_eligibility_built=context.get("calibration_aware_eligibility_built", False),
        ensemble_preparation_report_built=context.get("ensemble_preparation_report_built", False),
        ensemble_governance_built=context.get("ensemble_governance_built", False),
        non_activation_boundary_validated=context.get("non_activation_boundary_validated", False),
        model_cards_updated=context.get("model_cards_updated", False),
        readiness_gate_built=context.get("readiness_gate_built", False),
        readiness_gate_passed=context.get("readiness_gate_passed", False),
        ready_for_phase143=ready_for_phase143,
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
        ensemble_fitting_performed=False,
        final_ensemble_prediction_created=False,
        calibration_fitting_performed=False,
        calibrated_model_created=False,
        threshold_optimization_performed=False,
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
        valid_for_phase143=is_valid,
        risk_flags=list(set(risk_flags)),
        warnings=warnings,
        errors=errors,
        metadata={}
    )

def ingest_latest_ensemble_scaffolding_review_from_store(data_root: Path) -> EnsembleScaffoldingIngestionResult:
    # Placeholder for reading latest phase142 json
    # In real execution this would check `data/ml_research/ensemble_scaffolding/reviews/`
    return ingest_ensemble_scaffolding_review_payload({})

def extract_ensemble_scaffolding_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_ensemble_preparation_reports(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("preparation_reports", [])

def extract_ensemble_governance(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("ensemble_governance")

def extract_non_activation_ensemble_boundary(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("non_activation_boundary")

def extract_ensemble_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def ensemble_scaffolding_supports_phase143(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    res = ingest_ensemble_scaffolding_review_payload(payload)
    return res.valid_for_phase143, res.errors

def ensemble_scaffolding_ingestion_to_text(result: EnsembleScaffoldingIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Valid: {result.valid_for_phase143} - Errors: {len(result.errors)}"
