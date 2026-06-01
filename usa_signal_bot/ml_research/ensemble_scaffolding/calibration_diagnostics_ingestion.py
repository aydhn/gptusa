from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timezone
import json

from .phase142_models import (
    CalibrationDiagnosticsIngestionResult,
    create_calibration_diagnostics_ingestion_id,
    validate_calibration_diagnostics_ingestion_result,
    _now,
    EnsembleScaffoldingRiskFlag
)

def extract_calibration_diagnostics_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get('context')

def extract_calibration_diagnostics_reports(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get('preparation_reports', [])

def extract_post_training_validations(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get('validations', [])

def extract_calibration_governance(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get('governance')

def extract_calibration_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get('readiness_gate')

def calibration_diagnostics_supports_phase142(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    ready = True
    gate = payload.get('readiness_gate', {})
    if not gate.get('ready_for_phase142', False):
        ready = False
        errors.append("ready_for_phase142 is false in source payload")

    # Safe boundary checks
    for field in ['activation_allowed', 'strategy_activation_allowed', 'deployment_allowed',
                 'live_inference_enabled', 'online_inference_enabled', 'ensemble_fitting_performed',
                 'final_ensemble_prediction_created', 'calibration_fitting_performed',
                 'calibrated_model_created', 'threshold_optimization_performed',
                 'produces_trade_signal', 'produces_order_decision', 'produces_portfolio_weights',
                 'investment_advice']:
        if payload.get(field) is True or gate.get(field) is True:
            ready = False
            errors.append(f"Forbidden field '{field}' is True")

    for req_field in ['research_data_only', 'offline_ml_research_only']:
        if payload.get(req_field) is False or gate.get(req_field) is False:
            ready = False
            errors.append(f"Required field '{req_field}' is False")

    return ready, errors

def ingest_calibration_diagnostics_review_payload(payload: Dict[str, Any]) -> CalibrationDiagnosticsIngestionResult:
    ready, errors = calibration_diagnostics_supports_phase142(payload)
    gate = extract_calibration_readiness_gate(payload) or {}

    is_valid = True
    if not payload:
        is_valid = False
        errors.append("Empty payload")

    context = extract_calibration_diagnostics_context(payload)
    flags = []

    if context:
        if not context.get('model_comparison_ingested'): is_valid = False
        if not context.get('calibration_inputs_resolved'): is_valid = False
        if not context.get('reliability_bins_built'): is_valid = False
        if not context.get('calibration_metrics_built'): is_valid = False
        if not context.get('post_training_validation_built'): is_valid = False
        if not context.get('calibration_governance_built'): is_valid = False

    if not gate.get('readiness_gate_passed', False):
        is_valid = False

    res = CalibrationDiagnosticsIngestionResult(
        ingestion_id=create_calibration_diagnostics_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get('review_id'),
        source_context_id=context.get('context_id') if context else None,
        available=bool(payload),
        model_comparison_ingested=context.get('model_comparison_ingested', False) if context else False,
        comparison_artifacts_loaded=context.get('comparison_artifacts_loaded', False) if context else False,
        calibration_inputs_resolved=context.get('calibration_inputs_resolved', False) if context else False,
        reliability_bins_built=context.get('reliability_bins_built', False) if context else False,
        calibration_metrics_built=context.get('calibration_metrics_built', False) if context else False,
        brier_decomposition_built=context.get('brier_decomposition_built', False) if context else False,
        score_distribution_built=context.get('score_distribution_built', False) if context else False,
        class_balance_built=context.get('class_balance_built', False) if context else False,
        post_training_validation_built=context.get('post_training_validation_built', False) if context else False,
        calibration_governance_built=context.get('calibration_governance_built', False) if context else False,
        model_cards_updated=context.get('model_cards_updated', False) if context else False,
        readiness_gate_built=bool(gate),
        readiness_gate_passed=gate.get('readiness_gate_passed', False),
        ready_for_phase142=ready,
        metadata_only=payload.get('metadata_only', True),
        research_data_only=payload.get('research_data_only', True),
        offline_ml_research_only=payload.get('offline_ml_research_only', True),
        activation_allowed=payload.get('activation_allowed', False),
        strategy_activation_allowed=payload.get('strategy_activation_allowed', False),
        deployment_allowed=payload.get('deployment_allowed', False),
        active_paper_enabled=payload.get('active_paper_enabled', False),
        broker_execution_enabled=payload.get('broker_execution_enabled', False),
        order_creation_enabled=payload.get('order_creation_enabled', False),
        paper_state_mutation_enabled=payload.get('paper_state_mutation_enabled', False),
        telegram_real_send_enabled=payload.get('telegram_real_send_enabled', False),
        scraping_enabled=payload.get('scraping_enabled', False),
        html_parse_enabled=payload.get('html_parse_enabled', False),
        paid_api_enabled=payload.get('paid_api_enabled', False),
        dashboard_enabled=payload.get('dashboard_enabled', False),
        network_default_enabled=payload.get('network_default_enabled', False),
        daemon_started=payload.get('daemon_started', False),
        scheduler_enabled=payload.get('scheduler_enabled', False),
        live_inference_enabled=payload.get('live_inference_enabled', False),
        online_inference_enabled=payload.get('online_inference_enabled', False),
        calibration_fitting_performed=payload.get('calibration_fitting_performed', False),
        calibrated_model_created=payload.get('calibrated_model_created', False),
        threshold_optimization_performed=payload.get('threshold_optimization_performed', False),
        heavy_ml_dependency_used=payload.get('heavy_ml_dependency_used', False),
        produces_trade_signal=payload.get('produces_trade_signal', False),
        produces_order_decision=payload.get('produces_order_decision', False),
        produces_portfolio_weights=payload.get('produces_portfolio_weights', False),
        investment_advice=payload.get('investment_advice', False),
        network_used=payload.get('network_used', False),
        paid_api_used=payload.get('paid_api_used', False),
        scraping_used=payload.get('scraping_used', False),
        html_parsing_used=payload.get('html_parsing_used', False),
        broker_used=payload.get('broker_used', False),
        order_created=payload.get('order_created', False),
        paper_state_mutated=payload.get('paper_state_mutated', False),
        telegram_real_sent=payload.get('telegram_real_sent', False),
        dashboard_started=payload.get('dashboard_started', False),
        valid_for_phase142=is_valid and ready,
        risk_flags=flags,
        warnings=[],
        errors=errors,
        metadata={}
    )

    # Enforce safe validations
    val_errs = validate_calibration_diagnostics_ingestion_result(res)
    if val_errs:
        res.valid_for_phase142 = False
        res.errors.extend(val_errs)

    return res

def ingest_latest_calibration_diagnostics_review_from_store(data_root: Path) -> CalibrationDiagnosticsIngestionResult:
    # Dummy mock for phase implementation
    p = data_root / "ml_research" / "calibration_diagnostics" / "reviews" / "latest.json"
    if p.exists():
        with open(p, "r") as f:
            data = json.load(f)
            return ingest_calibration_diagnostics_review_payload(data)

    return ingest_calibration_diagnostics_review_payload({})

def calibration_diagnostics_ingestion_to_text(result: CalibrationDiagnosticsIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Valid: {result.valid_for_phase142}"
