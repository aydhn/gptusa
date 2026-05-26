import json
from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.exceptions import FeatureFoundationValidationError
from usa_signal_bot.feature_engine.phase116_models import FeatureFoundationContext, FeatureFoundationFullReview

@dataclass
class FeatureFoundationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class FeatureFoundationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[FeatureFoundationValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_no_execution_language_in_feature_text(text: str) -> FeatureFoundationValidationReport:
    report = FeatureFoundationValidationReport(True, 0, 0, 0, 0, [], [], [])
    if not text:
        return report
    s = text.lower()
    unsafe = [
        "buy", "sell", "signal", "order", "broker", "live_order", "paper_order",
        "kesin al", "kesin sat", "garanti kâr", "strong buy", "strong sell", "aktif trading",
        "emir gönderildi", "paper'a alındı", "canlıya alındı"
    ]
    for u in unsafe:
        if u in s:
            report.valid = False
            report.error_count += 1
            report.errors.append(f"Unsafe execution language detected: {u}")
            report.issues.append(FeatureFoundationValidationIssue("ERROR", None, f"Unsafe language: {u}", {}))
    return report

def validate_no_sensitive_data_in_feature_payload(payload: dict[str, Any]) -> FeatureFoundationValidationReport:
    report = FeatureFoundationValidationReport(True, 0, 0, 0, 0, [], [], [])
    unsafe_keys = ["api_key", "token", "secret", "password", "broker_order_id", "live_order_id", "sent_to_broker"]
    for k in payload.keys():
        if any(u in k.lower() for u in unsafe_keys):
            report.valid = False
            report.error_count += 1
            report.errors.append(f"Sensitive key detected: {k}")
            report.issues.append(FeatureFoundationValidationIssue("ERROR", k, f"Sensitive key: {k}", {}))
    return report

def validate_no_unsafe_feature_fields(payload: dict[str, Any]) -> FeatureFoundationValidationReport:
    report = FeatureFoundationValidationReport(True, 0, 0, 0, 0, [], [], [])
    booleans_to_block = [
        "activation_allowed", "active_paper_enabled", "broker_execution_enabled",
        "order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "scraping_enabled", "html_parse_enabled", "paid_api_enabled", "dashboard_enabled",
        "network_default_enabled", "network_used", "paid_api_used", "scraping_used",
        "html_parsing_used", "broker_used", "order_created", "paper_state_mutated",
        "telegram_real_sent", "dashboard_started", "produces_trade_signal", "produces_order_decision"
    ]
    for k in booleans_to_block:
        if payload.get(k, False):
            report.valid = False
            report.blocked_count += 1
            report.errors.append(f"Unsafe feature field activated: {k}")
            report.issues.append(FeatureFoundationValidationIssue("BLOCK", k, f"Field {k} is True", {}))
    return report

def validate_feature_foundation_context_report(item: FeatureFoundationContext) -> FeatureFoundationValidationReport:
    from usa_signal_bot.feature_engine.phase116_models import feature_foundation_context_to_dict
    payload = feature_foundation_context_to_dict(item)
    return validate_no_unsafe_feature_fields(payload)

def validate_feature_foundation_full_review_report(item: FeatureFoundationFullReview) -> FeatureFoundationValidationReport:
    from usa_signal_bot.feature_engine.phase116_models import feature_foundation_full_review_to_dict
    payload = feature_foundation_full_review_to_dict(item)

    r1 = validate_no_unsafe_feature_fields(payload.get("context", {}))
    r2 = validate_no_sensitive_data_in_feature_payload(payload)

    report = FeatureFoundationValidationReport(True, 0, 0, 0, 0, [], [], [])

    if not r1.valid:
        report.valid = False
        report.errors.extend(r1.errors)
        report.issues.extend(r1.issues)

    if not r2.valid:
        report.valid = False
        report.errors.extend(r2.errors)
        report.issues.extend(r2.issues)

    return report

def feature_foundation_validation_report_to_text(report: FeatureFoundationValidationReport) -> str:
    return f"Valid: {report.valid}\nErrors: {len(report.errors)}"

def assert_feature_foundation_validation_valid(report: FeatureFoundationValidationReport) -> None:
    if not report.valid:
        raise FeatureFoundationValidationError(f"Validation failed: {report.errors}")
