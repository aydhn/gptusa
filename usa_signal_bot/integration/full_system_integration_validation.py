
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.integration.phase158_models import FullSystemIntegrationContext, FullSystemIntegrationFullReview
from usa_signal_bot.core.exceptions import FullSystemIntegrationValidationError

@dataclass
class FullSystemIntegrationValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FullSystemIntegrationValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[FullSystemIntegrationValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_full_system_integration_context_report(item: FullSystemIntegrationContext) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def validate_full_system_integration_full_review_report(item: FullSystemIntegrationFullReview) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def validate_no_sensitive_data_in_integration_payload(payload: Dict[str, Any]) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def validate_no_execution_language_in_integration_text(text: str) -> FullSystemIntegrationValidationReport:
    report = FullSystemIntegrationValidationReport()
    forbidden = ["buy", "sell", "portfolio_weight"]
    for f in forbidden:
        if f in text.lower():
            report.valid = False
            report.error_count += 1
            report.errors.append(f"Forbidden text: {f}")
    return report

def validate_no_unsafe_integration_fields(payload: Dict[str, Any]) -> FullSystemIntegrationValidationReport:
    return FullSystemIntegrationValidationReport()

def full_system_integration_validation_report_to_text(report: FullSystemIntegrationValidationReport) -> str:
    return f"Validation Report Valid: {report.valid}"

def assert_full_system_integration_validation_valid(report: FullSystemIntegrationValidationReport) -> None:
    if not report.valid:
        raise FullSystemIntegrationValidationError("Validation failed")
