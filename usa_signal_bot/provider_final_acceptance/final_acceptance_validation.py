from dataclasses import dataclass
from typing import Any
import json
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFinalAcceptanceContext,
    ProviderFinalAcceptanceFullReview
)
from usa_signal_bot.core.exceptions import FinalAcceptanceValidationError

@dataclass
class ProviderFinalAcceptanceValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class ProviderFinalAcceptanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ProviderFinalAcceptanceValidationIssue]
    warnings: list[str]
    errors: list[str]

def _build_report(issues: list[ProviderFinalAcceptanceValidationIssue], warnings: list[str], errors: list[str]) -> ProviderFinalAcceptanceValidationReport:
    return ProviderFinalAcceptanceValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=sum(1 for i in issues if i.severity == "BLOCK"),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_provider_final_acceptance_context_report(item: ProviderFinalAcceptanceContext) -> ProviderFinalAcceptanceValidationReport:
    errors = []
    issues = []

    if item.activation_allowed:
        errors.append("activation_allowed is true")
        issues.append(ProviderFinalAcceptanceValidationIssue("BLOCK", "activation_allowed", "Must be false", {}))
    if item.active_paper_enabled:
        errors.append("active_paper_enabled is true")
        issues.append(ProviderFinalAcceptanceValidationIssue("BLOCK", "active_paper_enabled", "Must be false", {}))
    if item.broker_execution_enabled:
        errors.append("broker_execution_enabled is true")
        issues.append(ProviderFinalAcceptanceValidationIssue("BLOCK", "broker_execution_enabled", "Must be false", {}))
    if item.order_creation_enabled:
        errors.append("order_creation_enabled is true")
        issues.append(ProviderFinalAcceptanceValidationIssue("BLOCK", "order_creation_enabled", "Must be false", {}))
    if item.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled is true")
        issues.append(ProviderFinalAcceptanceValidationIssue("BLOCK", "paper_state_mutation_enabled", "Must be false", {}))
    if item.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled is true")
        issues.append(ProviderFinalAcceptanceValidationIssue("BLOCK", "telegram_real_send_enabled", "Must be false", {}))

    return _build_report(issues, [], errors)

def validate_provider_final_acceptance_full_review_report(item: ProviderFinalAcceptanceFullReview) -> ProviderFinalAcceptanceValidationReport:
    return validate_provider_final_acceptance_context_report(item.context)

def validate_no_sensitive_data_in_final_acceptance_payload(payload: dict[str, Any]) -> ProviderFinalAcceptanceValidationReport:
    errors = []
    s_payload = json.dumps(payload).lower()
    for sensitive in ["api_key", "secret", "password", "token", "broker_order_id", "live_order_id"]:
        if sensitive in s_payload:
            errors.append(f"Sensitive keyword '{sensitive}' found in payload.")
    return _build_report([ProviderFinalAcceptanceValidationIssue("BLOCK", None, e, {}) for e in errors], [], errors)

def validate_no_execution_language_in_final_acceptance_text(text: str) -> ProviderFinalAcceptanceValidationReport:
    errors = []
    text_lower = text.lower()
    bad_phrases = [
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "canlıya alındı", "kesin al", "kesin sat", "garanti kâr",
        "buy signal", "sell signal", "strong buy", "strong sell", "sent to broker"
    ]
    for p in bad_phrases:
        if p in text_lower:
            errors.append(f"Execution language '{p}' found in text.")
    return _build_report([ProviderFinalAcceptanceValidationIssue("BLOCK", None, e, {}) for e in errors], [], errors)

def validate_no_unsafe_final_acceptance_fields(payload: dict[str, Any]) -> ProviderFinalAcceptanceValidationReport:
    return validate_no_sensitive_data_in_final_acceptance_payload(payload)

def provider_final_acceptance_validation_report_to_text(report: ProviderFinalAcceptanceValidationReport) -> str:
    status = "VALID" if report.valid else "INVALID"
    return f"Validation [{status}] - Errors: {report.error_count}, Blocks: {report.blocked_count}"

def assert_provider_final_acceptance_validation_valid(report: ProviderFinalAcceptanceValidationReport) -> None:
    if not report.valid:
        raise FinalAcceptanceValidationError(f"Validation failed: {report.errors}")
