from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime, timezone
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeRegistryIngestionResult,
    create_runtime_registry_ingestion_id,
    validate_runtime_registry_ingestion_result
)
from usa_signal_bot.core.enums import RuntimeServiceGraphRiskFlag

def ingest_runtime_registry_review_payload(payload: Dict[str, Any]) -> RuntimeRegistryIngestionResult:
    registry = extract_normalized_runtime_registry(payload)
    available = registry is not None
    is_valid, phase_warnings = runtime_registry_supports_phase103(payload)

    registry_normalized = payload.get("registry_normalized", False)
    provider_interfaces_ready = payload.get("provider_interfaces_ready", False)
    safety_policy_valid = payload.get("safety_policy_valid", False)

    warnings = list(phase_warnings)
    errors = []
    risk_flags = []

    if not available:
        risk_flags.append(RuntimeServiceGraphRiskFlag.RUNTIME_REGISTRY_MISSING)
        errors.append("Runtime registry payload is missing normalized data")

    if not registry_normalized:
        errors.append("Registry is not normalized")

    if not provider_interfaces_ready:
        warnings.append("Provider interfaces not fully ready")

    if not safety_policy_valid:
        errors.append("Safety policy is invalid")

    activation_allowed = payload.get("activation_allowed", False)
    active_paper_enabled = payload.get("active_paper_enabled", False)
    broker_execution_enabled = payload.get("broker_execution_enabled", False)
    paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", False)
    telegram_real_send_enabled = payload.get("telegram_real_send_enabled", False)
    scraping_enabled = payload.get("scraping_enabled", False)
    dashboard_enabled = payload.get("dashboard_enabled", False)

    if activation_allowed or active_paper_enabled or broker_execution_enabled or paper_state_mutation_enabled or telegram_real_send_enabled or scraping_enabled or dashboard_enabled:
        errors.append("Safety violations detected in payload")
        risk_flags.append(RuntimeServiceGraphRiskFlag.RUNTIME_REGISTRY_INVALID)

    valid_for_phase103 = available and registry_normalized and safety_policy_valid and len(errors) == 0

    result = RuntimeRegistryIngestionResult(
        ingestion_id=create_runtime_registry_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        available=available,
        registry_normalized=registry_normalized,
        provider_interfaces_ready=provider_interfaces_ready,
        safety_policy_valid=safety_policy_valid,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        valid_for_phase103=valid_for_phase103,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
        metadata={"original_payload_keys": list(payload.keys())}
    )

    try:
        validate_runtime_registry_ingestion_result(result)
    except ValueError as e:
        result.valid_for_phase103 = False
        result.errors.append(str(e))

    return result

def ingest_latest_runtime_registry_review_from_store(data_root: Path) -> RuntimeRegistryIngestionResult:
    # Simulates loading from Phase 102
    return ingest_runtime_registry_review_payload({})

def extract_normalized_runtime_registry(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("normalized_registry")

def extract_provider_manifests(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    registry = extract_normalized_runtime_registry(payload)
    if not registry:
        return []
    return registry.get("provider_interfaces", [])

def runtime_registry_supports_phase103(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if not payload:
        return False, ["Payload is empty"]
    return True, warnings

def runtime_registry_ingestion_to_text(result: RuntimeRegistryIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id}: Valid={result.valid_for_phase103}"
