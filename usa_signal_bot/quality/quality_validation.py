"""Quality System Validation Rules."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.exceptions import QualityValidationError
from usa_signal_bot.quality.quality_models import (
    ResearchQualityScorecard,
    ProductionReadinessGateResult,
    SystemAcceptanceResult
)

@dataclass
class QualityValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class QualityValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[QualityValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_scorecard_report(scorecard: ResearchQualityScorecard) -> QualityValidationReport:
    issues = []
    if scorecard.overall_score is not None:
        if scorecard.overall_score < 0 or scorecard.overall_score > 100:
            issues.append(QualityValidationIssue("ERROR", "overall_score", f"Score {scorecard.overall_score} out of bounds."))

    return QualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "WARNING"),
        error_count=sum(1 for i in issues if i.severity == "ERROR"),
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_gate_result_report(result: ProductionReadinessGateResult) -> QualityValidationReport:
    return QualityValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, issues=[], warnings=[], errors=[])

def validate_acceptance_result_report(result: SystemAcceptanceResult) -> QualityValidationReport:
    return QualityValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, issues=[], warnings=[], errors=[])

def validate_no_live_execution_approval(result: SystemAcceptanceResult) -> QualityValidationReport:
    issues = []
    summary_lower = result.acceptance_summary.lower()

    forbidden_terms = ["live approved", "broker approved", "kesin al", "kesin sat", "garanti"]

    for term in forbidden_terms:
        if term in summary_lower:
            issues.append(QualityValidationIssue("ERROR", "acceptance_summary", f"Forbidden term found: {term}"))

    return QualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_no_investment_advice_language_in_quality(text: str) -> QualityValidationReport:
    issues = []
    text_lower = text.lower()

    forbidden_terms = ["kesin al", "kesin sat", "garanti", "investment advice"]

    for term in forbidden_terms:
        if term in text_lower:
            issues.append(QualityValidationIssue("ERROR", "text", f"Forbidden term found: {term}"))

    return QualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_no_sensitive_data_in_quality_payload(payload: Dict[str, Any]) -> QualityValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    if "token" in payload_str or "api_key" in payload_str or "secret" in payload_str:
        issues.append(QualityValidationIssue("ERROR", "payload", "Potentially sensitive token or key found in quality payload."))

    return QualityValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def quality_validation_report_to_text(report: QualityValidationReport) -> str:
    if report.valid:
        return "Validation PASS"
    return f"Validation FAIL: {report.error_count} errors, {report.warning_count} warnings. {'; '.join(report.errors)}"

def assert_quality_valid(report: QualityValidationReport) -> None:
    if not report.valid:
        raise QualityValidationError(quality_validation_report_to_text(report))
