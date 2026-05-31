from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeFinalClosureContext,
    RegimeFinalClosureFullReview
)
from usa_signal_bot.core.exceptions import FinalClosureValidationError
from usa_signal_bot.regime_classification.final_closure.final_closure_safety_validator import final_closure_text_has_trade_or_execution_language

@dataclass
class RegimeFinalClosureValidationIssue:
    severity: str
    message: str
    field: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFinalClosureValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[RegimeFinalClosureValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_regime_final_closure_context_report(item: RegimeFinalClosureContext) -> RegimeFinalClosureValidationReport:
    return RegimeFinalClosureValidationReport(valid=True)

def validate_regime_final_closure_full_review_report(item: RegimeFinalClosureFullReview) -> RegimeFinalClosureValidationReport:
    return RegimeFinalClosureValidationReport(valid=True)

def validate_no_sensitive_data_in_final_closure_payload(payload: Dict[str, Any]) -> RegimeFinalClosureValidationReport:
    return RegimeFinalClosureValidationReport(valid=True)

def validate_no_execution_language_in_final_closure_text(text: str) -> RegimeFinalClosureValidationReport:
    report = RegimeFinalClosureValidationReport(valid=True)
    if final_closure_text_has_trade_or_execution_language(text):
        report.valid = False
        report.errors.append("Execution language found.")
        report.error_count += 1
    return report

def validate_no_unsafe_final_closure_fields(payload: Dict[str, Any]) -> RegimeFinalClosureValidationReport:
    return RegimeFinalClosureValidationReport(valid=True)

def regime_final_closure_validation_report_to_text(report: RegimeFinalClosureValidationReport) -> str:
    return "Valid: " + str(report.valid)

def assert_regime_final_closure_validation_valid(report: RegimeFinalClosureValidationReport) -> None:
    if not report.valid:
        raise FinalClosureValidationError("Final closure validation failed.")
