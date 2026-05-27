from typing import Any
from dataclasses import dataclass, field
import json

from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FactorCompositionContext,
    FactorCompositionFullReview
)
from usa_signal_bot.feature_engine.factor_composition.factor_composition_safety_validator import (
    validate_factor_composition_context_safety,
    factor_composition_text_has_trade_or_execution_language
)

@dataclass
class FactorCompositionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorCompositionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[FactorCompositionValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def _create_report(issues: list[FactorCompositionValidationIssue]) -> FactorCompositionValidationReport:
    warnings = [i for i in issues if i.severity == "WARNING"]
    errors = [i for i in issues if i.severity == "ERROR"]
    blocks = [i for i in issues if i.severity == "BLOCK"]

    return FactorCompositionValidationReport(
        valid=len(errors) == 0 and len(blocks) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocks),
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors + blocks]
    )

def validate_factor_composition_context_report(item: FactorCompositionContext) -> FactorCompositionValidationReport:
    issues = []

    safety_errors = validate_factor_composition_context_safety(item)
    for e in safety_errors:
        issues.append(FactorCompositionValidationIssue("BLOCK", "safety", e))

    return _create_report(issues)

def validate_factor_composition_full_review_report(item: FactorCompositionFullReview) -> FactorCompositionValidationReport:
    return validate_factor_composition_context_report(item.context)

def validate_no_sensitive_data_in_factor_composition_payload(payload: dict[str, Any]) -> FactorCompositionValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()

    for sensitive in ["api_key", "token", "secret", "password", "broker_order_id", "live_order_id", "real_fill_id"]:
        if sensitive in payload_str:
            issues.append(FactorCompositionValidationIssue("BLOCK", "payload", f"Sensitive key detected: {sensitive}"))

    return _create_report(issues)

def validate_no_execution_language_in_factor_composition_text(text: str) -> FactorCompositionValidationReport:
    issues = []
    if factor_composition_text_has_trade_or_execution_language(text):
        issues.append(FactorCompositionValidationIssue("BLOCK", "text", "Execution or trade language detected in text"))
    return _create_report(issues)

def validate_no_unsafe_factor_composition_fields(payload: dict[str, Any]) -> FactorCompositionValidationReport:
    issues = []
    for field in [
        "activation_allowed", "active_paper_enabled", "broker_execution_enabled",
        "order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "scraping_enabled", "html_parse_enabled", "paid_api_enabled", "dashboard_enabled",
        "network_default_enabled", "produces_trade_signal", "produces_order_decision",
        "produces_portfolio_weights", "network_used", "paid_api_used", "scraping_used",
        "html_parsing_used", "broker_used", "order_created", "paper_state_mutated",
        "telegram_real_sent", "dashboard_started"
    ]:
        if payload.get(field, False):
            issues.append(FactorCompositionValidationIssue("BLOCK", field, f"Unsafe field {field} is true"))

    return _create_report(issues)

def factor_composition_validation_report_to_text(report: FactorCompositionValidationReport) -> str:
    lines = [
        f"Validation Report:",
        f"  Valid: {report.valid}",
        f"  Issues: {report.issue_count} (Errors: {report.error_count}, Blocked: {report.blocked_count}, Warnings: {report.warning_count})"
    ]
    if report.errors:
        lines.append("  Errors/Blocks:")
        for e in report.errors:
            lines.append(f"    - {e}")
    return "\n".join(lines)

def assert_factor_composition_validation_valid(report: FactorCompositionValidationReport) -> None:
    if not report.valid:
        from usa_signal_bot.core.exceptions import FactorCompositionValidationError
        raise FactorCompositionValidationError(f"Validation failed with {report.error_count} errors, {report.blocked_count} blocks. Details: {factor_composition_validation_report_to_text(report)}")
