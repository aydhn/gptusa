from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineMLScaffoldingContext,
    BaselineMLScaffoldingFullReview
)
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_scaffolding_schema_validator import _has_forbidden_semantics
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_scaffolding_safety_validator import baseline_scaffolding_text_has_trade_or_execution_language

@dataclass
class BaselineScaffoldingValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BaselineScaffoldingValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[BaselineScaffoldingValidationIssue]
    warnings: List[str]
    errors: List[str]

def _build_report(issues: List[BaselineScaffoldingValidationIssue], valid: bool) -> BaselineScaffoldingValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity in ("ERROR", "BLOCKED")]
    return BaselineScaffoldingValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_baseline_scaffolding_context_report(item: BaselineMLScaffoldingContext) -> BaselineScaffoldingValidationReport:
    issues = []
    if item.training_started:
        issues.append(BaselineScaffoldingValidationIssue("BLOCKED", "training_started", "Training not allowed in Phase 138"))
    if item.prediction_started:
        issues.append(BaselineScaffoldingValidationIssue("BLOCKED", "prediction_started", "Prediction not allowed in Phase 138"))
    if item.activation_allowed:
        issues.append(BaselineScaffoldingValidationIssue("BLOCKED", "activation_allowed", "Activation not allowed"))
    return _build_report(issues, len(issues) == 0)

def validate_baseline_scaffolding_full_review_report(item: BaselineMLScaffoldingFullReview) -> BaselineScaffoldingValidationReport:
    return validate_baseline_scaffolding_context_report(item.context)

def validate_no_sensitive_data_in_baseline_scaffolding_payload(payload: Dict[str, Any]) -> BaselineScaffoldingValidationReport:
    issues = []
    s = str(payload).lower()
    for secret in ["api_key", "secret", "password", "token"]:
        if secret in s:
            issues.append(BaselineScaffoldingValidationIssue("WARNING", None, f"Potential sensitive data '{secret}' found"))
    return _build_report(issues, len([i for i in issues if i.severity == "BLOCKED"]) == 0)

def validate_no_execution_language_in_baseline_scaffolding_text(text: str) -> BaselineScaffoldingValidationReport:
    issues = []
    if baseline_scaffolding_text_has_trade_or_execution_language(text):
        issues.append(BaselineScaffoldingValidationIssue("BLOCKED", None, "Execution language found in text"))
    return _build_report(issues, len(issues) == 0)

def validate_no_unsafe_baseline_scaffolding_fields(payload: Dict[str, Any]) -> BaselineScaffoldingValidationReport:
    issues = []
    for k in payload.keys():
        if _has_forbidden_semantics(k) and "signal" not in k.lower():
            issues.append(BaselineScaffoldingValidationIssue("BLOCKED", k, f"Forbidden field name '{k}'"))
    return _build_report(issues, len(issues) == 0)

def baseline_scaffolding_validation_report_to_text(report: BaselineScaffoldingValidationReport) -> str:
    out = [f"Valid: {report.valid}", f"Errors: {report.error_count}", f"Blocked: {report.blocked_count}"]
    for e in report.errors: out.append(f" - {e}")
    return "\n".join(out)

def assert_baseline_scaffolding_validation_valid(report: BaselineScaffoldingValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Validation failed: {report.errors}")
