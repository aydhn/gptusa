from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeTransitionValidationError
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionContext,
    RegimeTransitionFullReview
)

@dataclass
class RegimeTransitionValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeTransitionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RegimeTransitionValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_no_sensitive_data_in_regime_transition_payload(payload: Dict[str, Any]) -> RegimeTransitionValidationReport:
    report = RegimeTransitionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    for k in payload.keys():
        kl = k.lower()
        if "secret" in kl or "password" in kl or "token" in kl or "api_key" in kl:
            report.valid = False
            report.error_count += 1
            report.errors.append(f"Sensitive data found in key: {k}")
    return report

def validate_no_unsafe_regime_transition_fields(payload: Dict[str, Any]) -> RegimeTransitionValidationReport:
    report = RegimeTransitionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    unsafe_keys = ["activation_allowed", "broker_execution_enabled", "deployment_allowed"]
    for k, v in payload.items():
        if k in unsafe_keys and v is True:
            report.valid = False
            report.error_count += 1
            report.errors.append(f"Unsafe field {k} is True")
    return report

def validate_no_execution_language_in_regime_transition_text(text: str) -> RegimeTransitionValidationReport:
    from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_safety_validator import regime_diagnostics_text_has_trade_or_execution_language
    report = RegimeTransitionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    if regime_diagnostics_text_has_trade_or_execution_language(text):
        report.valid = False
        report.error_count += 1
        report.errors.append("Execution language found in text.")
    return report

def validate_regime_transition_context_report(item: RegimeTransitionContext) -> RegimeTransitionValidationReport:
    from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_safety_validator import validate_regime_transition_context_safety
    report = RegimeTransitionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    errs = validate_regime_transition_context_safety(item)
    if errs:
        report.valid = False
        report.error_count += len(errs)
        report.errors.extend(errs)
    return report

def validate_regime_transition_full_review_report(item: RegimeTransitionFullReview) -> RegimeTransitionValidationReport:
    return validate_regime_transition_context_report(item.context)

def assert_regime_transition_validation_valid(report: RegimeTransitionValidationReport) -> None:
    if not report.valid:
        raise RegimeTransitionValidationError(f"Validation failed: {report.errors}")

def regime_transition_validation_report_to_text(report: RegimeTransitionValidationReport) -> str:
    lines = [
        f"Validation Report [Valid: {report.valid}]",
        f"Errors: {report.error_count}, Warnings: {report.warning_count}"
    ]
    if report.errors:
        lines.append("Errors:")
        for e in report.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
