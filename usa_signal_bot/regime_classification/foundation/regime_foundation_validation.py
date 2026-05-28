import re
from dataclasses import dataclass, field
from typing import Any, Dict, List

from usa_signal_bot.regime_classification.foundation.phase126_models import RegimeFoundationContext, RegimeFoundationFullReview
from usa_signal_bot.regime_classification.foundation.regime_foundation_safety_validator import validate_regime_foundation_context_safety
from usa_signal_bot.regime_classification.foundation.regime_non_activation_boundary import check_safe_language

@dataclass
class RegimeFoundationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class RegimeFoundationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RegimeFoundationValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_no_unsafe_regime_foundation_fields(payload: dict[str, Any]) -> RegimeFoundationValidationReport:
    issues = []

    for f in ["activation_allowed", "strategy_activation_allowed", "deployment_allowed",
              "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
              "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
              "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
              "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
              "investment_advice", "network_used", "paid_api_used", "scraping_used", "html_parsing_used",
              "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "dashboard_started"]:
        if payload.get(f, False):
            issues.append(RegimeFoundationValidationIssue(
                severity="BLOCKED",
                field=f,
                message=f"Forbidden field {f} is True",
                details={}
            ))

    sensitive_keys = ["api_key", "token", "secret", "password", "broker_order_id", "live_order_id", "sent_to_broker"]
    for k in sensitive_keys:
        if k in payload:
            issues.append(RegimeFoundationValidationIssue(
                severity="BLOCKED",
                field=k,
                message=f"Sensitive field {k} found in payload",
                details={}
            ))

    forbidden_cols = ["buy_signal", "sell_signal", "portfolio_weight", "target_weight", "allocation", "deploy", "production_patch"]
    for k, v in payload.items():
        if isinstance(v, str) and v.lower() in forbidden_cols:
             issues.append(RegimeFoundationValidationIssue(
                severity="BLOCKED",
                field=k,
                message=f"Forbidden column name {v} found in payload",
                details={}
            ))

    blocked_count = len([i for i in issues if i.severity == "BLOCKED"])
    error_count = len([i for i in issues if i.severity == "ERROR"])
    warning_count = len([i for i in issues if i.severity == "WARNING"])

    errors = [i.message for i in issues if i.severity in ("ERROR", "BLOCKED")]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return RegimeFoundationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=warning_count,
        error_count=error_count,
        blocked_count=blocked_count,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_no_sensitive_data_in_regime_foundation_payload(payload: dict[str, Any]) -> RegimeFoundationValidationReport:
    return validate_no_unsafe_regime_foundation_fields(payload)

def validate_no_execution_language_in_regime_foundation_text(text: str) -> RegimeFoundationValidationReport:
    issues = []
    if not check_safe_language(text):
        issues.append(RegimeFoundationValidationIssue(
            severity="BLOCKED",
            field=None,
            message="Unsafe language detected in text",
            details={}
        ))

    errors = [i.message for i in issues if i.severity in ("ERROR", "BLOCKED")]
    return RegimeFoundationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_regime_foundation_context_report(item: RegimeFoundationContext) -> RegimeFoundationValidationReport:
    from dataclasses import asdict
    payload = asdict(item)
    report1 = validate_no_unsafe_regime_foundation_fields(payload)

    issues = report1.issues
    errors = report1.errors

    ctx_errors = validate_regime_foundation_context_safety(item)
    for err in ctx_errors:
        issues.append(RegimeFoundationValidationIssue(severity="ERROR", field=None, message=err, details={}))
        errors.append(err)

    return RegimeFoundationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=report1.warning_count,
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=report1.warnings,
        errors=errors
    )

def validate_regime_foundation_full_review_report(item: RegimeFoundationFullReview) -> RegimeFoundationValidationReport:
    from dataclasses import asdict
    payload = asdict(item)
    return validate_no_unsafe_regime_foundation_fields(payload)

def regime_foundation_validation_report_to_text(report: RegimeFoundationValidationReport) -> str:
    lines = [
        f"Validation Valid: {report.valid}",
        f"Issues: {report.issue_count} (Blocked: {report.blocked_count}, Errors: {report.error_count})"
    ]
    if report.errors:
        lines.append("Errors:")
        for err in report.errors:
            lines.append(f"  - {err}")
    return "\n".join(lines)

def assert_regime_foundation_validation_valid(report: RegimeFoundationValidationReport) -> None:
    if not report.valid:
        from usa_signal_bot.core.exceptions import RegimeFoundationValidationError
        raise RegimeFoundationValidationError(f"Validation failed with {report.error_count} errors.")
