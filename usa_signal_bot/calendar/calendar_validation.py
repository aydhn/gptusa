"""Calendar validation logic."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.exceptions import CalendarValidationError
from usa_signal_bot.calendar.calendar_models import (
    CalendarReviewResult,
    SessionValidationResult,
    MarketHoliday,
    MarketEarlyClose
)
from usa_signal_bot.core.enums import SessionValidationStatus

@dataclass
class CalendarValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class CalendarValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[CalendarValidationIssue]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_calendar_review_report(result: CalendarReviewResult) -> CalendarValidationReport:
    issues = []

    if result.errors:
        for err in result.errors:
            issues.append(CalendarValidationIssue(severity="ERROR", field=None, message=err))

    for sv in result.session_validations:
        if sv.status == SessionValidationStatus.INVALID:
            issues.append(CalendarValidationIssue(severity="ERROR", field=sv.symbol, message="Session validation INVALID"))
        elif sv.status == SessionValidationStatus.WARNING:
            issues.append(CalendarValidationIssue(severity="WARNING", field=sv.symbol, message="Session validation WARNING"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return CalendarValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_session_validation_report_report(result: SessionValidationResult) -> CalendarValidationReport:
    issues = []

    if result.status == SessionValidationStatus.INVALID:
        issues.append(CalendarValidationIssue(severity="ERROR", field="status", message="Session validation is INVALID"))
    elif result.status == SessionValidationStatus.WARNING:
        issues.append(CalendarValidationIssue(severity="WARNING", field="status", message="Session validation is WARNING"))

    for err in result.errors:
        issues.append(CalendarValidationIssue(severity="ERROR", field=None, message=err))
    for wrn in result.warnings:
        issues.append(CalendarValidationIssue(severity="WARNING", field=None, message=wrn))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return CalendarValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_holiday_files(holidays: list[MarketHoliday], early_closes: list[MarketEarlyClose]) -> CalendarValidationReport:
    issues = []

    holiday_dates = set()
    for h in holidays:
        if h.date in holiday_dates:
            issues.append(CalendarValidationIssue(severity="WARNING", field="date", message=f"Duplicate holiday date: {h.date}"))
        holiday_dates.add(h.date)

    early_close_dates = set()
    for c in early_closes:
        if c.date in early_close_dates:
            issues.append(CalendarValidationIssue(severity="WARNING", field="date", message=f"Duplicate early close date: {c.date}"))
        early_close_dates.add(c.date)

    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return CalendarValidationReport(
        valid=True,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=0,
        blocked_count=0,
        issues=issues,
        warnings=warnings,
        errors=[]
    )

def validate_no_sensitive_data_in_calendar_payload(payload: dict[str, Any]) -> CalendarValidationReport:
    payload_str = str(payload).lower()
    issues = []

    suspicious_keywords = ["api_key", "secret", "password", "token", "credentials"]
    for kw in suspicious_keywords:
        if kw in payload_str:
            issues.append(CalendarValidationIssue(severity="ERROR", field=None, message=f"Potential sensitive data leak detected: '{kw}'"))

    errors = [i.message for i in issues if i.severity == "ERROR"]

    return CalendarValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_live_execution_language_in_calendar(text: str) -> CalendarValidationReport:
    text_lower = text.lower()
    issues = []

    forbidden_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "investment advice"]
    for phrase in forbidden_phrases:
        if phrase in text_lower:
            issues.append(CalendarValidationIssue(severity="ERROR", field=None, message=f"Live execution/advice language detected: '{phrase}'"))

    errors = [i.message for i in issues if i.severity == "ERROR"]

    return CalendarValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def calendar_validation_report_to_text(report: CalendarValidationReport) -> str:
    lines = [
        f"Calendar Validation Report: {'VALID' if report.valid else 'INVALID'}",
        f"  Issues: {report.issue_count} (Errors: {report.error_count}, Warnings: {report.warning_count})"
    ]
    if report.errors:
        lines.append("  Errors:")
        for e in report.errors:
            lines.append(f"    - {e}")
    if report.warnings:
        lines.append("  Warnings:")
        for w in report.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)

def assert_calendar_valid(report: CalendarValidationReport) -> None:
    if not report.valid:
        raise CalendarValidationError("Calendar validation failed:\n" + "\n".join(report.errors))
