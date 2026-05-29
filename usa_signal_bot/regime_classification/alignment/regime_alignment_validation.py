from typing import Any
from dataclasses import dataclass, field
import json
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeAlignmentContext, RegimeAlignmentFullReview
)
from usa_signal_bot.core.exceptions import RegimeAlignmentValidationError

@dataclass
class RegimeAlignmentValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAlignmentValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[RegimeAlignmentValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_regime_alignment_context_report(item: RegimeAlignmentContext) -> RegimeAlignmentValidationReport:
    issues = []
    from usa_signal_bot.regime_classification.alignment.compatibility_safety_validator import validate_regime_alignment_context_safety
    from usa_signal_bot.regime_classification.alignment.compatibility_schema_validator import validate_alignment_context_schema

    sf = validate_regime_alignment_context_safety(item)
    sc = validate_alignment_context_schema(item)

    for e in sf + sc:
        issues.append(RegimeAlignmentValidationIssue("ERROR", None, e))

    return _build_report(issues)

def validate_regime_alignment_full_review_report(item: RegimeAlignmentFullReview) -> RegimeAlignmentValidationReport:
    if not item.context:
        return _build_report([RegimeAlignmentValidationIssue("ERROR", "context", "Missing context")])
    return validate_regime_alignment_context_report(item.context)

def validate_no_sensitive_data_in_regime_alignment_payload(payload: dict[str, Any]) -> RegimeAlignmentValidationReport:
    issues = []
    s = json.dumps(payload).lower()
    for k in ["api_key", "secret", "password", "token"]:
        if k in s:
            issues.append(RegimeAlignmentValidationIssue("ERROR", None, f"Sensitive key {k} found"))
    return _build_report(issues)

def validate_no_execution_language_in_regime_alignment_text(text: str) -> RegimeAlignmentValidationReport:
    from usa_signal_bot.regime_classification.alignment.compatibility_safety_validator import alignment_text_has_trade_or_execution_language
    issues = []
    if alignment_text_has_trade_or_execution_language(text):
        issues.append(RegimeAlignmentValidationIssue("ERROR", None, "Execution language found"))
    return _build_report(issues)

def validate_no_unsafe_regime_alignment_fields(payload: dict[str, Any]) -> RegimeAlignmentValidationReport:
    issues = []
    s = json.dumps(payload).lower()
    from usa_signal_bot.regime_classification.alignment.compatibility_schema_validator import FORBIDDEN_FRAGMENTS
    for f in FORBIDDEN_FRAGMENTS:
        if f in s and f != "signal":
            issues.append(RegimeAlignmentValidationIssue("ERROR", None, f"Forbidden fragment {f} found"))
    return _build_report(issues)

def _build_report(issues: list[RegimeAlignmentValidationIssue]) -> RegimeAlignmentValidationReport:
    warns = [i.message for i in issues if i.severity == "WARNING"]
    errs = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    return RegimeAlignmentValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=len(warns),
        error_count=len(errs),
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=warns,
        errors=errs
    )

def regime_alignment_validation_report_to_text(report: RegimeAlignmentValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_regime_alignment_validation_valid(report: RegimeAlignmentValidationReport) -> None:
    if not report.valid:
        raise RegimeAlignmentValidationError(f"Validation failed: {report.errors}")
