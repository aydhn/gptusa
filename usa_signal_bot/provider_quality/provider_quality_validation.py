import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.exceptions import ProviderQualityValidationError
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderQualityContext,
    ProviderQualityFullReview,
)


@dataclass
class ProviderQualityValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderQualityValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ProviderQualityValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def validate_no_unsafe_provider_quality_fields(
    payload: Dict[str, Any],
) -> ProviderQualityValidationReport:
    issues = []

    unsafe_flags = [
        "network_enabled_by_default",
        "network_used",
        "paid_api_enabled",
        "paid_api_used",
        "scraping_enabled",
        "scraping_used",
        "html_parse_enabled",
        "html_parsing_used",
        "broker_execution_enabled",
        "broker_used",
        "order_creation_enabled",
        "order_created",
        "paper_state_mutation_enabled",
        "paper_state_mutated",
        "telegram_real_send_enabled",
        "telegram_real_sent",
        "dashboard_enabled",
        "dashboard_started",
        "produces_trade_signal",
        "produces_order_decision",
    ]

    payload_str = json.dumps(payload).lower()

    for flag in unsafe_flags:
        # Check explicit dict if present
        if payload.get(flag) is True:
            issues.append(
                ProviderQualityValidationIssue(
                    "ERROR", flag, f"Unsafe execution flag '{flag}' must not be True"
                )
            )
        # Broad JSON text scan for nested truthiness
        elif f'"{flag}": true' in payload_str:
            issues.append(
                ProviderQualityValidationIssue(
                    "ERROR",
                    flag,
                    f"Unsafe execution flag '{flag}' detected as True in payload",
                )
            )

    return ProviderQualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues],
    )


def validate_no_execution_language_in_provider_quality_text(
    text: str,
) -> ProviderQualityValidationReport:
    unsafe_terms = [
        "emir gönderildi",
        "aktif trading başladı",
        "paper'a alındı",
        "kesin al",
        "kesin sat",
        "garanti kâr",
        "buy signal",
        "sell signal",
    ]
    issues = []
    text_lower = text.lower()

    for term in unsafe_terms:
        if term in text_lower:
            issues.append(
                ProviderQualityValidationIssue(
                    "ERROR", None, f"Unsafe execution language detected: '{term}'"
                )
            )

    return ProviderQualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues],
    )


def validate_no_sensitive_data_in_provider_quality_payload(
    payload: Dict[str, Any],
) -> ProviderQualityValidationReport:
    issues = []
    sensitive_keys_set = {
        "api_key",
        "token",
        "secret",
        "broker_order_id",
        "live_order_id",
        "sent_to_broker",
    }
    found_keys = set()
    stack = [payload]

    while stack:
        current = stack.pop()
        if type(current) is dict:
            for k, v in current.items():
                if type(k) is str:
                    k_lower = k.lower()
                    if k_lower in sensitive_keys_set:
                        found_keys.add(k_lower)
                t = type(v)
                if t is dict or t is list:
                    stack.append(v)
        elif type(current) is list:
            for item in current:
                t = type(item)
                if t is dict or t is list:
                    stack.append(item)

    sensitive_keys_ordered = [
        "api_key",
        "token",
        "secret",
        "broker_order_id",
        "live_order_id",
        "sent_to_broker",
    ]
    for k in sensitive_keys_ordered:
        if k in found_keys:
            issues.append(
                ProviderQualityValidationIssue(
                    "ERROR", k, f"Sensitive field detected: '{k}'"
                )
            )

    return ProviderQualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues],
    )


def validate_provider_quality_context_report(
    item: ProviderQualityContext,
) -> ProviderQualityValidationReport:
    # Just forward the payload checks
    from usa_signal_bot.provider_quality.phase109_models import (
        provider_quality_context_to_dict,
    )

    payload = provider_quality_context_to_dict(item)

    r1 = validate_no_unsafe_provider_quality_fields(payload)
    r2 = validate_no_sensitive_data_in_provider_quality_payload(payload)

    errors = r1.errors + r2.errors
    issues = r1.issues + r2.issues

    if not item.provider_quality_ready:
        errors.append("provider_quality_ready is False")

    return ProviderQualityValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        errors=errors,
    )


def validate_provider_quality_full_review_report(
    item: ProviderQualityFullReview,
) -> ProviderQualityValidationReport:
    from usa_signal_bot.provider_quality.phase109_models import (
        provider_quality_full_review_to_dict,
    )

    payload = provider_quality_full_review_to_dict(item)

    r1 = validate_no_unsafe_provider_quality_fields(payload)
    r2 = validate_no_sensitive_data_in_provider_quality_payload(payload)

    errors = r1.errors + r2.errors
    issues = r1.issues + r2.issues

    if not item.context.provider_quality_ready:
        errors.append("context.provider_quality_ready is False")

    return ProviderQualityValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        errors=errors,
    )


def assert_provider_quality_validation_valid(
    report: ProviderQualityValidationReport,
) -> None:
    if not report.valid:
        raise ProviderQualityValidationError(
            f"Provider Quality Validation failed with {report.error_count} errors: {report.errors}"
        )


def provider_quality_validation_report_to_text(
    report: ProviderQualityValidationReport,
) -> str:
    if report.valid:
        return "Provider Quality Validation: PASSED"
    return f"Provider Quality Validation: FAILED\n  " + "\n  ".join(report.errors)
