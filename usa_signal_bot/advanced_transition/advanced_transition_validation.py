from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from usa_signal_bot.advanced_transition.phase101_models import AdvancedTransitionContext, AdvancedTransitionFullReview

@dataclass
class AdvancedTransitionValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any]

@dataclass
class AdvancedTransitionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AdvancedTransitionValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_advanced_transition_context_report(context: AdvancedTransitionContext) -> AdvancedTransitionValidationReport:
    issues = []
    if context.activation_allowed:
        issues.append(AdvancedTransitionValidationIssue("ERROR", "activation_allowed", "Must be False", {}))
    return AdvancedTransitionValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_advanced_transition_full_review_report(review: AdvancedTransitionFullReview) -> AdvancedTransitionValidationReport:
    return validate_advanced_transition_context_report(review.context)

def validate_no_execution_capabilities_enabled(context: AdvancedTransitionContext) -> AdvancedTransitionValidationReport:
    issues = []
    if context.active_paper_enabled: issues.append(AdvancedTransitionValidationIssue("ERROR", "active_paper_enabled", "Must be False", {}))
    if context.broker_execution_enabled: issues.append(AdvancedTransitionValidationIssue("ERROR", "broker_execution_enabled", "Must be False", {}))
    return AdvancedTransitionValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_sensitive_data_in_advanced_transition_payload(payload: Dict[str, Any]) -> AdvancedTransitionValidationReport:
    issues = []
    keys = str(payload).lower()
    for sensitive in ["api_key", "secret", "token"]:
        if sensitive in keys:
            issues.append(AdvancedTransitionValidationIssue("ERROR", None, f"Found sensitive data: {sensitive}", {}))
    return AdvancedTransitionValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_execution_language_in_advanced_transition_text(text: str) -> AdvancedTransitionValidationReport:
    issues = []
    t = text.lower()
    for phrase in ["aktif trading başladı", "emir gönderildi", "canlıya alındı", "paper'a alındı", "garanti kâr", "kesin al"]:
        if phrase in t:
            issues.append(AdvancedTransitionValidationIssue("ERROR", None, f"Found execution language: {phrase}", {}))
    return AdvancedTransitionValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def advanced_transition_validation_report_to_text(report: AdvancedTransitionValidationReport) -> str:
    return f"Valid: {report.valid}\nErrors: {report.error_count}"

def assert_advanced_transition_valid(report: AdvancedTransitionValidationReport) -> None:
    from usa_signal_bot.core.exceptions import AdvancedTransitionValidationError
    if not report.valid:
        raise AdvancedTransitionValidationError(f"Validation failed: {report.errors}")
