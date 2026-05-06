import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.notifications.notification_models import NotificationMessage, NotificationConfig, NotificationDispatchResult
from usa_signal_bot.notifications.telegram_config import TelegramNotificationConfig, get_telegram_bot_token

@dataclass
class NotificationValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NotificationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[NotificationValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[NotificationValidationIssue]) -> NotificationValidationReport:
    warnings = [i.message for i in issues if i.severity == "warning"]
    errors = [i.message for i in issues if i.severity == "error"]

    return NotificationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_notification_message_report(message: NotificationMessage, config: Optional[NotificationConfig] = None) -> NotificationValidationReport:
    issues = []

    if not message.title and not message.body:
        issues.append(NotificationValidationIssue("error", "body", "Message must have a title or body"))

    if config and len(message.body) > config.max_message_length:
        issues.append(NotificationValidationIssue("error", "body", f"Message body exceeds max length ({len(message.body)} > {config.max_message_length})"))

    # Check execution language
    exec_lang_report = validate_no_execution_language(message)
    issues.extend(exec_lang_report.issues)

    return _create_report(issues)

def validate_dispatch_result(result: NotificationDispatchResult) -> NotificationValidationReport:
    issues = []

    expected_total = result.sent_count + result.failed_count + result.skipped_count + result.dry_run_count + result.suppressed_count
    if result.total_messages != expected_total:
        issues.append(NotificationValidationIssue(
            "error",
            "counts",
            f"Counts mismatch: total={result.total_messages}, sum={expected_total}"
        ))

    return _create_report(issues)

def validate_telegram_safety(config: TelegramNotificationConfig) -> NotificationValidationReport:
    issues = []

    if not config.allow_real_send:
        issues.append(NotificationValidationIssue("info", "allow_real_send", "Safe default: real send is disabled"))
    elif config.dry_run:
        issues.append(NotificationValidationIssue("info", "dry_run", "Safe mode: dry run is enabled"))
    else:
        if not get_telegram_bot_token(config):
            issues.append(NotificationValidationIssue("error", "token", "Token is missing while real send is enabled"))

    return _create_report(issues)

def validate_no_execution_language(message: NotificationMessage) -> NotificationValidationReport:
    issues = []

    forbidden_terms = ["kesin al", "kesin sat", "garanti", "buy now", "sell now", "guaranteed"]
    text_to_check = f"{message.title} {message.body}".lower()

    for term in forbidden_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', text_to_check):
            issues.append(NotificationValidationIssue(
                "error",
                "content",
                f"Potentially dangerous execution language detected: '{term}'"
            ))

    return _create_report(issues)

def validate_no_sensitive_token_leak(text: str, token: Optional[str] = None) -> NotificationValidationReport:
    issues = []
    if not token or len(token) < 10:
        return _create_report(issues)

    if token in text:
        issues.append(NotificationValidationIssue(
            "error",
            "security",
            "Sensitive token leak detected in text"
        ))

    return _create_report(issues)

def notification_validation_report_to_text(report: NotificationValidationReport) -> str:
    lines = [f"Validation Report: {'VALID' if report.valid else 'INVALID'}"]
    lines.append(f"Errors: {report.error_count} | Warnings: {report.warning_count}")

    for issue in report.issues:
        lines.append(f"[{issue.severity.upper()}] {issue.field or 'general'}: {issue.message}")

    return "\n".join(lines)

def assert_notification_valid(report: NotificationValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Notification validation failed:\n{notification_validation_report_to_text(report)}")
