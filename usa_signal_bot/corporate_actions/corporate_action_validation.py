"""Corporate action validation logic."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.exceptions import CorporateActionValidationError
from usa_signal_bot.corporate_actions.corporate_action_models import (
    CorporateActionEvent,
    AdjustedPriceValidationResult,
    CorporateActionGuardResult,
    CorporateActionReviewResult
)
from usa_signal_bot.core.enums import AdjustedPriceValidationStatus

@dataclass
class CorporateActionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class CorporateActionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[CorporateActionValidationIssue]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_corporate_action_events_report(events: list[CorporateActionEvent]) -> CorporateActionValidationReport:
    issues = []

    for e in events:
        if e.action_type.value == "SPLIT":
            if e.ratio_numerator is not None and e.ratio_numerator <= 0:
                issues.append(CorporateActionValidationIssue(severity="ERROR", field="ratio_numerator", message="Invalid split ratio (<= 0)"))
            if e.ratio_denominator is not None and e.ratio_denominator <= 0:
                issues.append(CorporateActionValidationIssue(severity="ERROR", field="ratio_denominator", message="Invalid split ratio (<= 0)"))
        elif e.action_type.value == "DIVIDEND":
            if e.value is not None and e.value < 0:
                issues.append(CorporateActionValidationIssue(severity="ERROR", field="value", message="Negative dividend detected"))

    errors = [i.message for i in issues if i.severity == "ERROR"]

    return CorporateActionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_adjusted_price_validation_report(result: AdjustedPriceValidationResult) -> CorporateActionValidationReport:
    issues = []

    if result.status == AdjustedPriceValidationStatus.INCONSISTENT:
        issues.append(CorporateActionValidationIssue(severity="ERROR", field="status", message="Adjusted price is INCONSISTENT"))
    elif result.status == AdjustedPriceValidationStatus.WARNING:
        issues.append(CorporateActionValidationIssue(severity="WARNING", field="status", message="Adjusted price has WARNING"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return CorporateActionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_corporate_action_guard_report(result: CorporateActionGuardResult) -> CorporateActionValidationReport:
    issues = []

    status_str = result.status.value if hasattr(result.status, "value") else str(result.status)
    if status_str in ["BLOCK_SIGNAL", "REVIEW_REQUIRED"]:
        issues.append(CorporateActionValidationIssue(severity="ERROR", field="status", message=f"Guard status is {status_str}"))
    elif status_str == "WARNING":
        issues.append(CorporateActionValidationIssue(severity="WARNING", field="status", message="Guard status is WARNING"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return CorporateActionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_corporate_action_review_report(result: CorporateActionReviewResult) -> CorporateActionValidationReport:
    issues = []

    for err in result.errors:
        issues.append(CorporateActionValidationIssue(severity="ERROR", field=None, message=err))

    for gr in result.guard_results:
        st = gr.status.value if hasattr(gr.status, "value") else str(gr.status)
        if st in ["BLOCK_SIGNAL", "REVIEW_REQUIRED"]:
            issues.append(CorporateActionValidationIssue(severity="ERROR", field=gr.symbol, message=f"Guard status {st}"))
        elif st == "WARNING":
            issues.append(CorporateActionValidationIssue(severity="WARNING", field=gr.symbol, message="Guard status WARNING"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return CorporateActionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_no_sensitive_data_in_corporate_action_payload(payload: dict[str, Any]) -> CorporateActionValidationReport:
    payload_str = str(payload).lower()
    issues = []
    suspicious = ["api_key", "secret", "password", "token", "credentials"]
    for kw in suspicious:
        if kw in payload_str:
            issues.append(CorporateActionValidationIssue(severity="ERROR", field=None, message=f"Potential sensitive data leak detected: '{kw}'"))
    errors = [i.message for i in issues if i.severity == "ERROR"]
    return CorporateActionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_live_execution_language_in_corporate_action(text: str) -> CorporateActionValidationReport:
    text_lower = text.lower()
    issues = []
    forbidden_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "investment advice"]
    for phrase in forbidden_phrases:
        if phrase in text_lower:
            issues.append(CorporateActionValidationIssue(severity="ERROR", field=None, message=f"Live execution/advice language detected: '{phrase}'"))
    errors = [i.message for i in issues if i.severity == "ERROR"]
    return CorporateActionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def corporate_action_validation_report_to_text(report: CorporateActionValidationReport) -> str:
    lines = [
        f"Corporate Action Validation: {'VALID' if report.valid else 'INVALID'}",
        f"  Issues: {report.issue_count} (Errors: {report.error_count}, Warnings: {report.warning_count})"
    ]
    for e in report.errors:
        lines.append(f"  ERROR: {e}")
    for w in report.warnings:
        lines.append(f"  WARN: {w}")
    return "\n".join(lines)

def assert_corporate_action_valid(report: CorporateActionValidationReport) -> None:
    if not report.valid:
        raise CorporateActionValidationError("Corporate action validation failed:\n" + "\n".join(report.errors))
