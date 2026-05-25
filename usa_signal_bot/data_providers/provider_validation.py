
from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderAbstractionContext, ProviderAbstractionFullReview
from usa_signal_bot.core.exceptions import ProviderValidationError

@dataclass
class ProviderValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ProviderValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_provider_abstraction_context_report(item: ProviderAbstractionContext) -> ProviderValidationReport:
    errs = []
    if item.activation_allowed: errs.append("activation_allowed true")
    if item.active_paper_enabled: errs.append("active_paper_enabled true")
    if item.broker_execution_enabled: errs.append("broker_execution_enabled true")
    if item.paper_state_mutation_enabled: errs.append("paper_state_mutation_enabled true")
    if item.telegram_real_send_enabled: errs.append("telegram_real_send_enabled true")
    if item.scraping_enabled: errs.append("scraping_enabled true")
    if item.html_parse_enabled: errs.append("html_parse_enabled true")
    if item.dashboard_enabled: errs.append("dashboard_enabled true")
    if item.paid_api_enabled: errs.append("paid_api_enabled true")
    if item.provider_network_fetch_enabled_now: errs.append("provider_network_fetch_enabled_now true")

    return ProviderValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=len(errs),
        errors=errs
    )

def validate_provider_abstraction_full_review_report(item: ProviderAbstractionFullReview) -> ProviderValidationReport:
    return validate_provider_abstraction_context_report(item.context)

def validate_no_sensitive_data_in_provider_payload(payload: dict[str, Any]) -> ProviderValidationReport:
    errs = []
    s = str(payload).lower()
    for w in ["api_key", "token", "secret", "broker_order_id", "live_order_id", "sent_to_broker"]:
        if w in s: errs.append(f"Sensitive data found: {w}")
    return ProviderValidationReport(valid=len(errs) == 0, issue_count=len(errs), warning_count=0, error_count=len(errs), blocked_count=len(errs), errors=errs)

def validate_no_execution_language_in_provider_text(text: str) -> ProviderValidationReport:
    errs = []
    t = text.lower()
    for w in ["emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "garanti kâr", "scrape", "parse html"]:
        if w in t: errs.append(f"Execution language found: {w}")
    return ProviderValidationReport(valid=len(errs) == 0, issue_count=len(errs), warning_count=0, error_count=len(errs), blocked_count=len(errs), errors=errs)

def validate_no_unsafe_provider_fields(payload: dict[str, Any]) -> ProviderValidationReport:
    errs = []
    if payload.get("network_fetch_enabled_now", False): errs.append("network_fetch_enabled_now true")
    if payload.get("credential_required_now", False): errs.append("credential_required_now true")
    if payload.get("scraping_required", False): errs.append("scraping_required true")
    if payload.get("html_parsing_required", False): errs.append("html_parsing_required true")
    if payload.get("broker_related", False): errs.append("broker_related true")
    if payload.get("order_related", False): errs.append("order_related true")
    return ProviderValidationReport(valid=len(errs) == 0, issue_count=len(errs), warning_count=0, error_count=len(errs), blocked_count=len(errs), errors=errs)

def provider_validation_report_to_text(report: ProviderValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_provider_validation_valid(report: ProviderValidationReport) -> None:
    if not report.valid:
        raise ProviderValidationError("Validation failed: " + ", ".join(report.errors))
