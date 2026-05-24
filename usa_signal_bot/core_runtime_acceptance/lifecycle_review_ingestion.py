from typing import Dict, Any, Optional, Tuple, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    LifecycleReviewIngestionResult,
    create_lifecycle_review_ingestion_id,
    _now,
    CoreRuntimeAcceptanceRiskFlag
)

def ingest_runtime_lifecycle_review_payload(payload: Dict[str, Any]) -> LifecycleReviewIngestionResult:
    result = LifecycleReviewIngestionResult(
        ingestion_id=create_lifecycle_review_ingestion_id(),
        created_at_utc=_now()
    )
    if not payload:
        result.valid_for_phase105 = False
        result.warnings.append("Empty payload")
        return result

    result.available = True
    result.lifecycle_ready = payload.get("lifecycle_ready", False)
    result.ready_for_phase105 = payload.get("ready_for_phase105", False)
    result.readiness_gate_passed = payload.get("readiness_gate_passed", False)
    result.startup_checks_passed = payload.get("startup_checks_passed", False)
    result.all_required_services_ready = payload.get("all_required_services_ready", False)

    result.activation_allowed = payload.get("activation_allowed", False)
    result.active_paper_enabled = payload.get("active_paper_enabled", False)
    result.broker_execution_enabled = payload.get("broker_execution_enabled", False)
    result.paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", False)
    result.telegram_real_send_enabled = payload.get("telegram_real_send_enabled", False)
    result.scraping_enabled = payload.get("scraping_enabled", False)
    result.dashboard_enabled = payload.get("dashboard_enabled", False)

    result.execution_performed = payload.get("execution_performed", False)
    result.network_used = payload.get("network_used", False)
    result.broker_used = payload.get("broker_used", False)
    result.order_created = payload.get("order_created", False)
    result.paper_state_mutated = payload.get("paper_state_mutated", False)
    result.telegram_real_sent = payload.get("telegram_real_sent", False)
    result.scraping_used = payload.get("scraping_used", False)
    result.dashboard_started = payload.get("dashboard_started", False)

    is_valid, reasons = lifecycle_review_supports_phase105(payload)
    result.valid_for_phase105 = is_valid
    result.errors.extend(reasons)

    return result

def ingest_latest_runtime_lifecycle_review_from_store(data_root: Any) -> LifecycleReviewIngestionResult:
    # Dummy mock for phase 104 output read
    return ingest_runtime_lifecycle_review_payload({"lifecycle_ready": True, "ready_for_phase105": True, "readiness_gate_passed": True, "startup_checks_passed": True, "all_required_services_ready": True})

def extract_runtime_lifecycle_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("lifecycle_context")

def extract_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def lifecycle_review_supports_phase105(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    is_valid = True

    if not payload.get("lifecycle_ready", False):
        reasons.append("lifecycle_ready is false")
        is_valid = False
    if not payload.get("ready_for_phase105", False):
        reasons.append("ready_for_phase105 is false")
        is_valid = False
    if not payload.get("readiness_gate_passed", False):
        reasons.append("readiness_gate_passed is false")
        is_valid = False
    if not payload.get("startup_checks_passed", False):
        reasons.append("startup_checks_passed is false")
        is_valid = False

    for key in ["activation_allowed", "active_paper_enabled", "broker_execution_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled", "dashboard_enabled"]:
        if payload.get(key, False):
            reasons.append(f"{key} is true")
            is_valid = False

    for key in ["execution_performed", "network_used", "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "scraping_used", "dashboard_started"]:
        if payload.get(key, False):
            reasons.append(f"{key} is true")
            is_valid = False

    return is_valid, reasons

def lifecycle_review_ingestion_to_text(result: LifecycleReviewIngestionResult) -> str:
    return f"LifecycleReviewIngestionResult(valid={result.valid_for_phase105})"
