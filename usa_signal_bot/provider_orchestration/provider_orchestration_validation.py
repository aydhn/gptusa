from dataclasses import dataclass, field
from typing import Any
import json
from usa_signal_bot.provider_orchestration.phase110_models import (
    ProviderOrchestrationContext, ProviderOrchestrationFullReview,
    provider_orchestration_context_to_dict, provider_orchestration_full_review_to_dict
)

@dataclass
class ProviderOrchestrationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderOrchestrationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ProviderOrchestrationValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def _validate_payload(payload: dict[str, Any]) -> ProviderOrchestrationValidationReport:
    report = ProviderOrchestrationValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)

    # Exec validations
    for k in ["produces_trade_signal", "produces_order_decision", "allow_network", "network_required",
              "network_allowed_now", "network_used", "paid_api_used", "scraping_used", "html_parsing_used",
              "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "dashboard_started"]:
        if payload.get(k, False):
            report.valid = False
            report.error_count += 1
            report.issues.append(ProviderOrchestrationValidationIssue("ERROR", k, f"{k} must be False"))

    # Text validations
    text_rep = json.dumps(payload).lower()
    unsafe_terms = ["api_key", "token", "secret", "broker_order_id", "live_order_id", "sent_to_broker",
                    "emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "kesin sat",
                    "garanti kâr", "buy signal", "sell signal"]
    for term in unsafe_terms:
        if term in text_rep:
            report.valid = False
            report.error_count += 1
            report.issues.append(ProviderOrchestrationValidationIssue("ERROR", "payload_text", f"Unsafe term found: {term}"))

    return report

def validate_provider_orchestration_context_report(item: ProviderOrchestrationContext) -> ProviderOrchestrationValidationReport:
    return _validate_payload(provider_orchestration_context_to_dict(item))

def validate_provider_orchestration_full_review_report(item: ProviderOrchestrationFullReview) -> ProviderOrchestrationValidationReport:
    return _validate_payload(provider_orchestration_full_review_to_dict(item))

def validate_no_sensitive_data_in_provider_orchestration_payload(payload: dict[str, Any]) -> ProviderOrchestrationValidationReport:
    return _validate_payload(payload)

def validate_no_execution_language_in_provider_orchestration_text(text: str) -> ProviderOrchestrationValidationReport:
    report = ProviderOrchestrationValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    unsafe_terms = ["api_key", "token", "secret", "broker_order_id", "live_order_id", "sent_to_broker",
                    "emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "kesin sat",
                    "garanti kâr", "buy signal", "sell signal"]
    lower_text = text.lower()
    for term in unsafe_terms:
        if term in lower_text:
            report.valid = False
            report.error_count += 1
            report.issues.append(ProviderOrchestrationValidationIssue("ERROR", "text", f"Unsafe term found: {term}"))
    return report

def validate_no_unsafe_orchestration_fields(payload: dict[str, Any]) -> ProviderOrchestrationValidationReport:
    return _validate_payload(payload)

def provider_orchestration_validation_report_to_text(report: ProviderOrchestrationValidationReport) -> str:
    lines = [f"Valid: {report.valid}"]
    for issue in report.issues:
        lines.append(f"[{issue.severity}] {issue.field}: {issue.message}")
    return "\n".join(lines)

def assert_provider_orchestration_validation_valid(report: ProviderOrchestrationValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Provider Orchestration Validation failed: {report.error_count} errors")
