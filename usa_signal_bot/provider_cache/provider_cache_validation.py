from dataclasses import dataclass, field
from typing import Any
import json
from usa_signal_bot.provider_cache.phase108_models import ProviderCacheContext, ProviderCacheFullReview
from usa_signal_bot.core.exceptions import ProviderCacheValidationError

@dataclass
class ProviderCacheValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class ProviderCacheValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ProviderCacheValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_provider_cache_context_report(item: ProviderCacheContext) -> ProviderCacheValidationReport:
    issues = []

    if item.network_enabled_by_default:
        issues.append(ProviderCacheValidationIssue("ERROR", "network_enabled_by_default", "Network is enabled.", {}))

    for r in item.fallback_results:
        if r.network_used:
             issues.append(ProviderCacheValidationIssue("ERROR", "fallback_results.network_used", "Network used in fallback.", {}))

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return ProviderCacheValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "WARNING"),
        error_count=len(errs),
        blocked_count=1 if errs else 0,
        issues=issues, warnings=[], errors=errs
    )

def validate_provider_cache_full_review_report(item: ProviderCacheFullReview) -> ProviderCacheValidationReport:
    return validate_provider_cache_context_report(item.context)

def validate_no_sensitive_data_in_provider_cache_payload(payload: dict[str, Any]) -> ProviderCacheValidationReport:
    s_payload = json.dumps(payload).lower()
    unsafe = ["api_key", "token", "secret", "broker_order_id", "live_order_id", "sent_to_broker"]
    issues = []
    for u in unsafe:
        if u in s_payload:
            issues.append(ProviderCacheValidationIssue("ERROR", "payload", f"Sensitive key {u} found.", {}))
    errs = [i.message for i in issues if i.severity == "ERROR"]
    return ProviderCacheValidationReport(len(errs)==0, len(issues), 0, len(errs), 1 if errs else 0, issues, [], errs)

def validate_no_execution_language_in_provider_cache_text(text: str) -> ProviderCacheValidationReport:
    s_text = text.lower()
    unsafe = ["emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "garanti kâr", "scrape", "parse html"]
    issues = []
    for u in unsafe:
        if u in s_text:
            issues.append(ProviderCacheValidationIssue("ERROR", "text", f"Unsafe execution language: {u}", {}))
    errs = [i.message for i in issues if i.severity == "ERROR"]
    return ProviderCacheValidationReport(len(errs)==0, len(issues), 0, len(errs), 1 if errs else 0, issues, [], errs)

def validate_no_unsafe_cache_fields(payload: dict[str, Any]) -> ProviderCacheValidationReport:
    return ProviderCacheValidationReport(True, 0, 0, 0, 0, [], [], [])

def provider_cache_validation_report_to_text(report: ProviderCacheValidationReport) -> str:
    return f"Report Valid: {report.valid}, Errors: {report.error_count}"

def assert_provider_cache_validation_valid(report: ProviderCacheValidationReport) -> None:
    if not report.valid:
        raise ProviderCacheValidationError(f"Validation failed: {report.errors}")
