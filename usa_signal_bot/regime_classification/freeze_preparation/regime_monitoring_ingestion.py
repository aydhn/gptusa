from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import json

from usa_signal_bot.core.enums import ResearchFreezeRiskFlag
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeMonitoringIngestionResult,
    create_regime_monitoring_ingestion_id,
    _now_utc_str
)

def extract_regime_monitoring_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_monitoring_baseline(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("baseline")

def extract_monitoring_snapshot(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("snapshot")

def extract_drift_tracking_result(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("drift_result")

def extract_context_degradation_diagnostics(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("degradation_diagnostics", [])

def extract_context_degradation_profiles(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("degradation_profiles", [])

def extract_monitoring_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def regime_monitoring_supports_phase134(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []

    if payload.get("activation_allowed"):
        errors.append("activation_allowed is True")
    if payload.get("deployment_allowed"):
        errors.append("deployment_allowed is True")
    if payload.get("produces_trade_signal"):
        errors.append("produces_trade_signal is True")
    if payload.get("investment_advice"):
        errors.append("investment_advice is True")

    return len(errors) == 0, errors

def ingest_regime_monitoring_review_payload(payload: Dict[str, Any], source_path: Optional[str] = None) -> RegimeMonitoringIngestionResult:
    review_id = payload.get("review_id")
    context_id = payload.get("context_id")

    supports, errors = regime_monitoring_supports_phase134(payload)

    ready = supports and payload.get("ready_for_phase134", False)

    res = RegimeMonitoringIngestionResult(
        ingestion_id=create_regime_monitoring_ingestion_id(),
        created_at_utc=_now_utc_str(),
        source_path=source_path,
        source_review_id=review_id,
        source_context_id=context_id,
        available=True,
        context_validation_ingested=True,
        artifacts_loaded=True,
        baseline_built=payload.get("baseline_built", True),
        snapshot_built=payload.get("snapshot_built", True),
        drift_tracked=payload.get("drift_tracked", True),
        degradation_diagnostics_built=payload.get("degradation_diagnostics_built", True),
        readiness_gate_built=payload.get("readiness_gate_built", True),
        readiness_gate_passed=payload.get("readiness_gate_passed", True),
        ready_for_phase134=ready,
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
        daemon_started=False,
        scheduler_enabled=False,
        valid_for_phase134=ready,
        risk_flags=[],
        warnings=[],
        errors=errors,
        metadata={}
    )

    if not ready:
        res.risk_flags.append(ResearchFreezeRiskFlag.PHASE133_NOT_READY)

    return res

def ingest_latest_regime_monitoring_review_from_store(data_root: Path) -> RegimeMonitoringIngestionResult:
    # dummy implementation for now
    return ingest_regime_monitoring_review_payload({})

def regime_monitoring_ingestion_to_text(result: RegimeMonitoringIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Ready: {result.ready_for_phase134}"
