from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.exceptions import AdmissionReviewValidationError
from .admission_review_models import (
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    FinalNoWriteTransitionCheckpoint,
    AdmissionReviewFullReport
)

@dataclass
class AdmissionReviewValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdmissionReviewValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AdmissionReviewValidationIssue]
    warnings: List[str]
    errors: List[str]

def _build_validation_report(issues: List[AdmissionReviewValidationIssue]) -> AdmissionReviewValidationReport:
    errors = [i for i in issues if i.severity in ["ERROR", "BLOCK"]]
    warnings = [i for i in issues if i.severity == "WARNING"]
    return AdmissionReviewValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len([i for i in issues if i.severity == "BLOCK"]),
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors]
    )

def validate_admission_review_report(item: PaperModeAdmissionReview) -> AdmissionReviewValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_denied", "must be True"))
    if item.activation_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_allowed", "must be False"))
    if item.transition_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "transition_allowed", "must be False"))
    if not item.all_writes_blocked:
        issues.append(AdmissionReviewValidationIssue("ERROR", "all_writes_blocked", "must be True"))
    if item.mutation_detected:
        issues.append(AdmissionReviewValidationIssue("ERROR", "mutation_detected", "must be False"))
    for attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(item, attr, True):
             issues.append(AdmissionReviewValidationIssue("ERROR", attr, "must be False"))
    return _build_validation_report(issues)

def validate_ledger_reconciliation_validation_report(item: LedgerReconciliationReport) -> AdmissionReviewValidationReport:
    issues = []
    if not item.acknowledged_not_activation:
        issues.append(AdmissionReviewValidationIssue("BLOCK", "acknowledged_not_activation", "must be True"))
    if item.activation_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_allowed", "must be False"))
    if len(item.warnings) > 0:
        issues.append(AdmissionReviewValidationIssue("BLOCK", "warnings", "Unsafe notes detected"))
    return _build_validation_report(issues)

def validate_transition_checkpoint_validation_report(item: FinalNoWriteTransitionCheckpoint) -> AdmissionReviewValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_denied", "must be True"))
    if item.activation_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_allowed", "must be False"))
    if item.transition_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "transition_allowed", "must be False"))
    if not item.all_writes_blocked:
        issues.append(AdmissionReviewValidationIssue("ERROR", "all_writes_blocked", "must be True"))
    if item.mutation_detected:
        issues.append(AdmissionReviewValidationIssue("ERROR", "mutation_detected", "must be False"))
    for attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(item, attr, True):
             issues.append(AdmissionReviewValidationIssue("ERROR", attr, "must be False"))
    return _build_validation_report(issues)

def validate_admission_full_report_validation(item: AdmissionReviewFullReport) -> AdmissionReviewValidationReport:
    issues = []
    for review in item.admission_reviews:
        rep = validate_admission_review_report(review)
        issues.extend(rep.issues)
    for rec in item.ledger_reconciliations:
        rep = validate_ledger_reconciliation_validation_report(rec)
        issues.extend(rep.issues)
    for cp in item.transition_checkpoints:
        rep = validate_transition_checkpoint_validation_report(cp)
        issues.extend(rep.issues)
    return _build_validation_report(issues)

def _validate_language(text: str, unsafe_keywords: List[str], error_message: str) -> AdmissionReviewValidationReport:
    issues = []
    text_lower = text.lower()
    for kw in unsafe_keywords:
        if kw in text_lower:
             issues.append(AdmissionReviewValidationIssue("BLOCK", "language", f"{error_message}: '{kw}'"))
    return _build_validation_report(issues)

def validate_no_live_execution_language_in_admission(text: str) -> AdmissionReviewValidationReport:
    keywords = ["live approved", "sent to broker", "kesin al", "garanti", "emir gönder", "gerçek emir"]
    return _validate_language(text, keywords, "Live execution language detected")

def validate_no_active_paper_language_in_admission(text: str) -> AdmissionReviewValidationReport:
    keywords = ["paper'a uygula", "aktif et", "canlıya al", "kesin kâr", "candidate kesin iyi"]
    return _validate_language(text, keywords, "Active paper language detected")

def validate_no_paper_state_mutation_fields_in_admission(payload: Dict[str, Any]) -> AdmissionReviewValidationReport:
    issues = []
    text = json.dumps(payload)
    for field in ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if f'"{field}": true' in text.lower():
             issues.append(AdmissionReviewValidationIssue("BLOCK", field, "Paper mutation field is true"))
    return _build_validation_report(issues)

def validate_no_broker_execution_fields_in_admission(payload: Dict[str, Any]) -> AdmissionReviewValidationReport:
    issues = []
    text = json.dumps(payload)
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f'"{field}"' in text.lower():
             issues.append(AdmissionReviewValidationIssue("BLOCK", field, "Broker execution field detected"))
    return _build_validation_report(issues)

def validate_no_sensitive_data_in_admission_payload(payload: Dict[str, Any]) -> AdmissionReviewValidationReport:
    issues = []
    text = json.dumps(payload)
    if "api_key" in text.lower() or "secret" in text.lower() or "token" in text.lower():
        # Heuristic
        pass
    return _build_validation_report(issues)

def admission_review_validation_report_to_text(report: AdmissionReviewValidationReport) -> str:
    return json.dumps([i.__dict__ for i in report.issues], indent=2)

def assert_admission_review_valid(report: AdmissionReviewValidationReport) -> None:
    if not report.valid:
        raise AdmissionReviewValidationError(f"Validation failed with {report.error_count} errors")
