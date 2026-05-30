from dataclasses import dataclass
from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringContext,
    RegimeMonitoringFullReview
)
from usa_signal_bot.regime_classification.monitoring.monitoring_safety_validator import validate_regime_monitoring_context_safety, monitoring_text_has_trade_or_execution_language
from usa_signal_bot.regime_classification.monitoring.monitoring_schema_validator import validate_no_forbidden_monitoring_columns
from usa_signal_bot.core.exceptions import RegimeMonitoringValidationError

@dataclass
class RegimeMonitoringValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any]

@dataclass
class RegimeMonitoringValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RegimeMonitoringValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_regime_monitoring_context_report(item: RegimeMonitoringContext) -> RegimeMonitoringValidationReport:
    errors = validate_regime_monitoring_context_safety(item)
    issues = [RegimeMonitoringValidationIssue("ERROR", None, e, {}) for e in errors]
    return RegimeMonitoringValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_regime_monitoring_full_review_report(item: RegimeMonitoringFullReview) -> RegimeMonitoringValidationReport:
    if item.context:
        return validate_regime_monitoring_context_report(item.context)
    return RegimeMonitoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_monitoring_payload(payload: Dict[str, Any]) -> RegimeMonitoringValidationReport:
    # Dummy implementation
    return RegimeMonitoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_execution_language_in_monitoring_text(text: str) -> RegimeMonitoringValidationReport:
    if monitoring_text_has_trade_or_execution_language(text):
         return RegimeMonitoringValidationReport(False, 1, 0, 1, 1, [RegimeMonitoringValidationIssue("ERROR", None, "Execution language detected", {})], [], ["Execution language detected"])
    return RegimeMonitoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_unsafe_monitoring_fields(payload: Dict[str, Any]) -> RegimeMonitoringValidationReport:
    columns = list(payload.keys())
    errors = validate_no_forbidden_monitoring_columns(columns)
    if errors:
         return RegimeMonitoringValidationReport(False, len(errors), 0, len(errors), len(errors), [RegimeMonitoringValidationIssue("ERROR", c, e, {}) for c, e in zip(columns, errors)], [], errors)
    return RegimeMonitoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def regime_monitoring_validation_report_to_text(report: RegimeMonitoringValidationReport) -> str:
    return f"Validation Valid: {report.valid}, Errors: {report.error_count}"

def assert_regime_monitoring_validation_valid(report: RegimeMonitoringValidationReport) -> None:
    if not report.valid:
        raise RegimeMonitoringValidationError(f"Validation failed: {report.errors}")
