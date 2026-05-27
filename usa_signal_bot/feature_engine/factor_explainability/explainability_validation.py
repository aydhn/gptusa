import json
from dataclasses import dataclass
from typing import Any

from usa_signal_bot.core.exceptions import ExplainabilityValidationError
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ExplainabilityContext,
    ExplainabilityFullReview
)
from usa_signal_bot.feature_engine.factor_explainability.explainability_safety_validator import (
    explainability_text_has_trade_or_execution_language
)

@dataclass
class ExplainabilityValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class ExplainabilityValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ExplainabilityValidationIssue]
    warnings: list[str]
    errors: list[str]

def _check_boolean_flags(item: Any, issues: list[ExplainabilityValidationIssue], errors: list[str]) -> None:
    flags_to_check = [
        "activation_allowed", "strategy_activation_allowed", "active_paper_enabled",
        "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled",
        "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "network_used", "paid_api_used", "scraping_used", "html_parsing_used",
        "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent",
        "dashboard_started", "produces_trade_signal", "produces_order_decision",
        "produces_portfolio_weights", "investment_advice"
    ]
    for flag in flags_to_check:
        if getattr(item, flag, False) is True:
            msg = f"{flag} is true"
            errors.append(msg)
            issues.append(ExplainabilityValidationIssue(severity="ERROR", field=flag, message=msg, details={}))

def validate_explainability_context_report(item: ExplainabilityContext) -> ExplainabilityValidationReport:
    issues = []
    errors = []

    _check_boolean_flags(item, issues, errors)

    if not item.report_qa_passed:
        errors.append("report_qa_passed is false")

    valid = len(errors) == 0
    return ExplainabilityValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_explainability_full_review_report(item: ExplainabilityFullReview) -> ExplainabilityValidationReport:
    return validate_explainability_context_report(item.context)

def validate_no_sensitive_data_in_explainability_payload(payload: dict[str, Any]) -> ExplainabilityValidationReport:
    issues = []
    errors = []
    payload_str = json.dumps(payload).lower()
    for sensitive in ["api_key", "token", "secret", "password"]:
        if sensitive in payload_str:
            errors.append(f"Sensitive data detected: {sensitive}")

    return ExplainabilityValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_execution_language_in_explainability_text(text: str) -> ExplainabilityValidationReport:
    issues = []
    errors = []

    if explainability_text_has_trade_or_execution_language(text):
        errors.append("Execution language detected")

    return ExplainabilityValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_unsafe_explainability_fields(payload: dict[str, Any]) -> ExplainabilityValidationReport:
    return validate_no_sensitive_data_in_explainability_payload(payload)

def explainability_validation_report_to_text(report: ExplainabilityValidationReport) -> str:
    return f"Explainability Validation Valid: {report.valid} ({report.error_count} errors)"

def assert_explainability_validation_valid(report: ExplainabilityValidationReport) -> None:
    if not report.valid:
        raise ExplainabilityValidationError(f"Explainability Validation failed: {report.errors}")
