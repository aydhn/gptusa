from dataclasses import dataclass, field
from typing import Any, Dict, List

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderRuntimeContext,
    ProviderRuntimeFullReview
)
from usa_signal_bot.core.exceptions import ProviderRuntimeValidationError


@dataclass
class ProviderRuntimeValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderRuntimeValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[ProviderRuntimeValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def validate_provider_runtime_context_report(item: ProviderRuntimeContext) -> ProviderRuntimeValidationReport:
    report = ProviderRuntimeValidationReport(valid=True)

    if not item.ingestion.provider_abstraction_ready:
        report.valid = False
        report.errors.append("provider_abstraction_ready must be True")
        report.issues.append(ProviderRuntimeValidationIssue("ERROR", "ingestion", "provider_abstraction_ready must be True"))

    if not item.metadata_only:
        report.valid = False
        report.errors.append("metadata_only must be True")
        report.issues.append(ProviderRuntimeValidationIssue("ERROR", "metadata_only", "metadata_only must be True"))

    if item.network_enabled_by_default:
        report.valid = False
        report.errors.append("network_enabled_by_default must be False")
        report.issues.append(ProviderRuntimeValidationIssue("ERROR", "network_enabled_by_default", "network_enabled_by_default must be False"))

    if item.paid_api_enabled:
        report.valid = False
        report.errors.append("paid_api_enabled must be False")
        report.issues.append(ProviderRuntimeValidationIssue("ERROR", "paid_api_enabled", "paid_api_enabled must be False"))

    report.error_count = len(report.errors)
    return report


def validate_provider_runtime_full_review_report(item: ProviderRuntimeFullReview) -> ProviderRuntimeValidationReport:
    return validate_provider_runtime_context_report(item.context)


def validate_no_sensitive_data_in_provider_runtime_payload(payload: Dict[str, Any]) -> ProviderRuntimeValidationReport:
    report = ProviderRuntimeValidationReport(valid=True)
    import json
    text = json.dumps(payload).lower()

    sensitive = ["api_key", "token", "secret", "password"]
    for s in sensitive:
        if s in text:
            report.valid = False
            report.errors.append(f"Sensitive data found: {s}")
            report.issues.append(ProviderRuntimeValidationIssue("ERROR", "payload", f"Sensitive data found: {s}"))

    report.error_count = len(report.errors)
    return report


def validate_no_execution_language_in_provider_runtime_text(text: str) -> ProviderRuntimeValidationReport:
    report = ProviderRuntimeValidationReport(valid=True)
    text = text.lower()

    banned = [
        "broker_order_id", "live_order_id", "sent_to_broker",
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "kesin al", "garanti kâr", "scrape", "parse html"
    ]

    for b in banned:
        if b in text:
            report.valid = False
            report.errors.append(f"Execution language found: {b}")
            report.issues.append(ProviderRuntimeValidationIssue("ERROR", "text", f"Execution language found: {b}"))

    report.error_count = len(report.errors)
    return report


def validate_no_unsafe_runtime_provider_fields(payload: Dict[str, Any]) -> ProviderRuntimeValidationReport:
    report = ProviderRuntimeValidationReport(valid=True)

    unsafe = [
        "activation_allowed", "active_paper_enabled", "broker_execution_enabled",
        "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "scraping_enabled", "html_parse_enabled", "dashboard_enabled",
        "paid_api_enabled", "provider_network_fetch_enabled_now",
        "network_enabled_by_default", "network_used", "paid_api_used",
        "scraping_used", "html_parsing_used", "broker_used", "order_created",
        "paper_state_mutated", "credential_required_now"
    ]

    def walk(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in unsafe and v is True:
                    report.valid = False
                    report.errors.append(f"Unsafe field set to True: {k}")
                    report.issues.append(ProviderRuntimeValidationIssue("ERROR", k, f"Unsafe field set to True: {k}"))
                walk(v)
        elif isinstance(d, list):
            for v in d:
                walk(v)

    walk(payload)

    report.error_count = len(report.errors)
    return report

def provider_runtime_validation_report_to_text(report: ProviderRuntimeValidationReport) -> str:
    lines = [
        "=== Provider Runtime Validation Report ===",
        f"Valid: {report.valid}",
        f"Error Count: {report.error_count}",
        ""
    ]
    if report.errors:
        lines.append("Errors:")
        for e in report.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)


def assert_provider_runtime_validation_valid(report: ProviderRuntimeValidationReport) -> None:
    if not report.valid:
        raise ProviderRuntimeValidationError("Provider runtime validation failed. Check report.")
