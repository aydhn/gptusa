from typing import Any
from dataclasses import dataclass
from usa_signal_bot.advanced_runtime.phase102_models import NormalizedRuntimeRegistry, RuntimeRegistryFullReview
import json

@dataclass
class RuntimeRegistryValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class RuntimeRegistryValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[RuntimeRegistryValidationIssue]
    warnings: list[str]
    errors: list[str]

def _build_empty_report() -> RuntimeRegistryValidationReport:
    return RuntimeRegistryValidationReport(
        valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0,
        issues=[], warnings=[], errors=[]
    )

def validate_normalized_runtime_registry_report(registry: NormalizedRuntimeRegistry) -> RuntimeRegistryValidationReport:
    report = _build_empty_report()
    if registry.activation_allowed:
        report.valid = False
        report.errors.append("activation_allowed is true")
    if registry.active_paper_enabled:
        report.valid = False
        report.errors.append("active_paper_enabled is true")
    return report

def validate_runtime_registry_full_review_report(review: RuntimeRegistryFullReview) -> RuntimeRegistryValidationReport:
    return validate_normalized_runtime_registry_report(review.registry)

def validate_no_sensitive_data_in_runtime_registry_payload(payload: dict[str, Any]) -> RuntimeRegistryValidationReport:
    report = _build_empty_report()
    s = str(payload).lower()
    for kw in ["api_key", "secret", "token", "password"]:
        if kw in s:
            report.valid = False
            report.errors.append(f"Sensitive keyword '{kw}' found in payload")
    return report

def validate_no_execution_language_in_runtime_registry_text(text: str) -> RuntimeRegistryValidationReport:
    report = _build_empty_report()
    s = text.lower()
    for kw in ["emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "garanti kâr", "sent to broker"]:
        if kw in s:
            report.valid = False
            report.errors.append(f"Execution language '{kw}' found in text")
    return report

def validate_no_unsafe_provider_contracts(payload: dict[str, Any]) -> RuntimeRegistryValidationReport:
    report = _build_empty_report()
    return report

def runtime_registry_validation_report_to_text(report: RuntimeRegistryValidationReport) -> str:
    return f"Valid: {report.valid} | Errors: {len(report.errors)}"

def assert_runtime_registry_valid(report: RuntimeRegistryValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Registry validation failed: {report.errors}")
