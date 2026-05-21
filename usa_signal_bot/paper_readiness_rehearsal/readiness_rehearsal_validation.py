import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    ReadinessRehearsalRun, FinalReviewLock, GuardedHandoffRegistryEntry, ReadinessRehearsalReview,
    validate_readiness_rehearsal_run, validate_final_review_lock, validate_guarded_handoff_registry_entry,
    validate_readiness_rehearsal_review
)

@dataclass
class ReadinessRehearsalValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessRehearsalValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ReadinessRehearsalValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[ReadinessRehearsalValidationIssue]) -> ReadinessRehearsalValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCKED"]

    return ReadinessRehearsalValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors + blocked
    )

def validate_rehearsal_run_report(item: ReadinessRehearsalRun) -> ReadinessRehearsalValidationReport:
    issues = []
    try:
        validate_readiness_rehearsal_run(item)
    except Exception as e:
        issues.append(ReadinessRehearsalValidationIssue("ERROR", "ReadinessRehearsalRun", str(e)))
    return _create_report(issues)

def validate_final_lock_report(item: FinalReviewLock) -> ReadinessRehearsalValidationReport:
    issues = []
    try:
        validate_final_review_lock(item)
    except Exception as e:
        issues.append(ReadinessRehearsalValidationIssue("ERROR", "FinalReviewLock", str(e)))
    return _create_report(issues)

def validate_handoff_entry_report(item: GuardedHandoffRegistryEntry) -> ReadinessRehearsalValidationReport:
    issues = []
    try:
        validate_guarded_handoff_registry_entry(item)
    except Exception as e:
        issues.append(ReadinessRehearsalValidationIssue("ERROR", "GuardedHandoffRegistryEntry", str(e)))
    return _create_report(issues)

def validate_readiness_rehearsal_review_report(item: ReadinessRehearsalReview) -> ReadinessRehearsalValidationReport:
    issues = []
    try:
        validate_readiness_rehearsal_review(item)
    except Exception as e:
        issues.append(ReadinessRehearsalValidationIssue("ERROR", "ReadinessRehearsalReview", str(e)))
    return _create_report(issues)

def validate_no_sensitive_data_in_readiness_rehearsal_payload(payload: Dict[str, Any]) -> ReadinessRehearsalValidationReport:
    issues = []
    payload_str = str(payload).lower()
    for secret_key in ["api_key", "secret", "password", "token"]:
        if secret_key in payload_str:
            issues.append(ReadinessRehearsalValidationIssue("BLOCKED", None, f"Potential secret leak detected: {secret_key}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_readiness_rehearsal(text: str) -> ReadinessRehearsalValidationReport:
    issues = []
    text_lower = text.lower()
    banned_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir", "kesin kâr", "candidate kesin iyi"]
    for phrase in banned_phrases:
        if phrase in text_lower:
            issues.append(ReadinessRehearsalValidationIssue("ERROR", None, f"Banned live execution language found: '{phrase}'"))
    return _create_report(issues)

def validate_no_active_paper_language_in_readiness_rehearsal(text: str) -> ReadinessRehearsalValidationReport:
    issues = []
    text_lower = text.lower()
    banned_phrases = ["paper'a uygula", "canlıya al", "aktif et", "paper trading enabled"]
    for phrase in banned_phrases:
        if phrase in text_lower:
            issues.append(ReadinessRehearsalValidationIssue("ERROR", None, f"Banned active paper language found: '{phrase}'"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_readiness_rehearsal(payload: Dict[str, Any]) -> ReadinessRehearsalValidationReport:
    issues = []
    banned_fields = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]
    for field_name in banned_fields:
        if field_name in payload:
            issues.append(ReadinessRehearsalValidationIssue("ERROR", field_name, f"Banned paper mutation field found: '{field_name}'"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_readiness_rehearsal(payload: Dict[str, Any]) -> ReadinessRehearsalValidationReport:
    issues = []
    banned_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for field_name in banned_fields:
        if field_name in payload:
            issues.append(ReadinessRehearsalValidationIssue("ERROR", field_name, f"Banned broker execution field found: '{field_name}'"))
    return _create_report(issues)

def readiness_rehearsal_validation_report_to_text(report: ReadinessRehearsalValidationReport) -> str:
    lines = [f"Validation Report: Valid={report.valid} | Issues={report.issue_count}"]
    for i in report.issues:
        lines.append(f" - [{i.severity}] {i.field or 'N/A'}: {i.message}")
    return "\n".join(lines)

def assert_readiness_rehearsal_valid(report: ReadinessRehearsalValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Readiness Rehearsal Validation Failed: {report.errors}")
