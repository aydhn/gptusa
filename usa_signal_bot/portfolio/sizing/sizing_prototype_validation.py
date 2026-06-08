from typing import Any
from dataclasses import dataclass, field
from usa_signal_bot.portfolio.sizing.phase154_models import SizingPrototypeContext, SizingPrototypeFullReview
from usa_signal_bot.portfolio.sizing.sizing_safety_validator import (
    sizing_payload_has_forbidden_fields, sizing_text_has_trade_or_execution_language
)
from usa_signal_bot.core.exceptions import SizingPrototypeValidationError

@dataclass
class SizingPrototypeValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingPrototypeValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: list[SizingPrototypeValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_sizing_prototype_context_report(item: SizingPrototypeContext) -> SizingPrototypeValidationReport:
    report = SizingPrototypeValidationReport()
    report.valid = item.ready_for_phase155
    if not report.valid:
        report.error_count += 1
        report.errors.append("Context is not ready for phase 155.")
    return report

def validate_sizing_prototype_full_review_report(item: SizingPrototypeFullReview) -> SizingPrototypeValidationReport:
    report = SizingPrototypeValidationReport()
    report.valid = item.phase155_readiness_gate.ready_for_phase155
    if not report.valid:
        report.error_count += 1
        report.errors.append("Review is not ready for phase 155.")
    return report

def validate_no_sensitive_data_in_sizing_payload(payload: dict[str, Any]) -> SizingPrototypeValidationReport:
    report = SizingPrototypeValidationReport(valid=True)
    if sizing_payload_has_forbidden_fields(payload):
        report.valid = False
        report.error_count += 1
        report.errors.append("Forbidden sizing fields found.")
    return report

def validate_no_execution_language_in_sizing_text(text: str) -> SizingPrototypeValidationReport:
    report = SizingPrototypeValidationReport(valid=True)
    if sizing_text_has_trade_or_execution_language(text):
        report.valid = False
        report.error_count += 1
        report.errors.append("Execution language found.")
    return report

def validate_no_unsafe_sizing_fields(payload: dict[str, Any]) -> SizingPrototypeValidationReport:
    return validate_no_sensitive_data_in_sizing_payload(payload)

def sizing_prototype_validation_report_to_text(report: SizingPrototypeValidationReport) -> str:
    return f"Sizing Validation Report: valid={report.valid}, errors={report.error_count}"

def assert_sizing_prototype_validation_valid(report: SizingPrototypeValidationReport) -> None:
    if not report.valid:
        raise SizingPrototypeValidationError(f"Sizing validation failed: {report.errors}")
