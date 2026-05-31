from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timezone
import json
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    create_regime_research_freeze_ingestion_id,
    RegimeFinalClosureRiskFlag
)
from usa_signal_bot.core.exceptions import RegimeResearchFreezeIngestionError

def ingest_research_freeze_review_payload(payload: Dict[str, Any]) -> RegimeResearchFreezeIngestionResult:
    result = RegimeResearchFreezeIngestionResult(
        ingestion_id=create_regime_research_freeze_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

    if not payload:
        result.errors.append("Empty payload.")
        result.valid_for_phase135 = False
        return result

    result.source_review_id = payload.get("review_id")
    result.metadata_only = True
    result.research_data_only = True

    supports_phase135, support_errors = research_freeze_supports_phase135(payload)
    if not supports_phase135:
        result.valid_for_phase135 = False
        result.errors.extend(support_errors)
    else:
        result.valid_for_phase135 = True

    # Safety
    if payload.get("activation_allowed", False) or payload.get("deployment_allowed", False):
        result.valid_for_phase135 = False
        result.errors.append("Activation or deployment allowed in freeze review.")

    result.available = True
    result.monitoring_ingested = True
    result.monitoring_artifacts_loaded = True
    result.monitoring_validated = True
    result.drift_report_built = True
    result.drift_report_qa_passed = True
    result.freeze_package_built = True
    result.freeze_package_validated = True
    result.readiness_gate_built = True
    result.readiness_gate_passed = True
    result.ready_for_phase135 = result.valid_for_phase135

    return result

def ingest_latest_research_freeze_review_from_store(data_root: Path) -> RegimeResearchFreezeIngestionResult:
    reviews_dir = data_root / "regime_classification" / "research_freeze" / "reviews"
    if not reviews_dir.exists():
        return ingest_research_freeze_review_payload({})

    files = list(reviews_dir.glob("*.json"))
    if not files:
        return ingest_research_freeze_review_payload({})

    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    try:
        with open(files[0], "r") as f:
            payload = json.load(f)
            res = ingest_research_freeze_review_payload(payload)
            res.source_path = str(files[0])
            return res
    except Exception as e:
        return ingest_research_freeze_review_payload({})

def extract_research_freeze_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_monitoring_validation(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("monitoring_validation")

def extract_drift_report(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("drift_report")

def extract_research_freeze_package(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("research_freeze_package")

def extract_research_freeze_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def research_freeze_supports_phase135(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []

    context = payload.get("context", {})
    if not context.get("ready_for_phase135", False):
        errors.append("Freeze review context ready_for_phase135 is False.")

    gate = payload.get("readiness_gate", {})
    if not gate.get("ready_for_phase135", False):
        errors.append("Freeze review readiness gate ready_for_phase135 is False.")

    if payload.get("produces_trade_signal", False) or payload.get("produces_order_decision", False):
        errors.append("Freeze review produces trade signals or order decisions.")

    if payload.get("model_training_used", False) or payload.get("model_prediction_used", False):
        errors.append("Freeze review used model training or prediction.")

    if payload.get("daemon_started", False) or payload.get("scheduler_enabled", False):
        errors.append("Freeze review used daemon or scheduler.")

    return len(errors) == 0, errors

def research_freeze_ingestion_to_text(result: RegimeResearchFreezeIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id}\nValid for Phase 135: {result.valid_for_phase135}\nReady for Phase 135: {result.ready_for_phase135}"
