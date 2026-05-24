from dataclasses import dataclass, field
from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    LifecycleReviewIngestionResult,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    DataProviderExpansionKickoffGate,
    CoreRuntimeAcceptanceFullReview
)

@dataclass
class CoreRuntimeAcceptanceValidationIssue:
    severity: str
    field: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoreRuntimeAcceptanceValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[CoreRuntimeAcceptanceValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _build_report(errors: List[str]) -> CoreRuntimeAcceptanceValidationReport:
    valid = len(errors) == 0
    return CoreRuntimeAcceptanceValidationReport(
        valid=valid,
        error_count=len(errors),
        errors=errors
    )

def validate_lifecycle_ingestion_payload(item: LifecycleReviewIngestionResult) -> CoreRuntimeAcceptanceValidationReport:
    errors = []
    if not item.lifecycle_ready: errors.append("lifecycle_ready is false")
    if not item.ready_for_phase105: errors.append("ready_for_phase105 is false")
    if getattr(item, 'activation_allowed', False): errors.append("activation_allowed is true")
    return _build_report(errors)

def validate_acceptance_report_payload(item: CoreRuntimeAcceptanceReport) -> CoreRuntimeAcceptanceValidationReport:
    errors = []
    if not item.core_runtime_accepted: errors.append("core_runtime_accepted is false")
    if getattr(item, 'activation_allowed', False): errors.append("activation_allowed is true")
    return _build_report(errors)

def validate_foundation_freeze_payload(item: AdvancedFoundationFreezeBundle) -> CoreRuntimeAcceptanceValidationReport:
    errors = []
    if not item.frozen: errors.append("frozen is false")
    if getattr(item, 'activation_allowed', False): errors.append("activation_allowed is true")
    return _build_report(errors)

def validate_provider_kickoff_gate_payload(item: DataProviderExpansionKickoffGate) -> CoreRuntimeAcceptanceValidationReport:
    errors = []
    if not item.ready_for_phase106: errors.append("ready_for_phase106 is false")
    if getattr(item, 'activation_allowed', False): errors.append("activation_allowed is true")
    return _build_report(errors)

def validate_core_runtime_acceptance_full_review_report(item: CoreRuntimeAcceptanceFullReview) -> CoreRuntimeAcceptanceValidationReport:
    return _build_report([])

def validate_no_sensitive_data_in_acceptance_payload(payload: Dict[str, Any]) -> CoreRuntimeAcceptanceValidationReport:
    errors = []
    import json
    text = json.dumps(payload)
    if "api_key" in text or "token" in text or "secret" in text:
        errors.append("contains sensitive key/token/secret")
    if "broker_order_id" in text or "live_order_id" in text or "sent_to_broker" in text:
        errors.append("contains real broker execution language")
    return _build_report(errors)

def validate_no_execution_language_in_acceptance_text(text: str) -> CoreRuntimeAcceptanceValidationReport:
    errors = []
    text_lower = text.lower()
    for forbidden in ["emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "garanti kâr", "canlıya alındı"]:
        if forbidden in text_lower:
            errors.append(f"contains forbidden execution language: {forbidden}")
    return _build_report(errors)

def core_runtime_acceptance_validation_report_to_text(report: CoreRuntimeAcceptanceValidationReport) -> str:
    return f"Validation: {'Valid' if report.valid else 'Invalid'}"

def assert_core_runtime_acceptance_valid(report: CoreRuntimeAcceptanceValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Validation failed: {report.errors}")
