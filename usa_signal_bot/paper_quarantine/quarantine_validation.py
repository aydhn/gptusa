import json
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import BridgeOperation
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    QuarantineEnrollmentReview,
)
from usa_signal_bot.core.exceptions import QuarantineValidationError

@dataclass
class QuarantineValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class QuarantineValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[QuarantineValidationIssue]
    warnings: list[str]
    errors: list[str]

def _check_broker_fields(payload: dict[str, Any]) -> list[QuarantineValidationIssue]:
    issues = []
    bad_keys = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]

    def _check(d: dict, path: str = ""):
        for k, v in d.items():
            current_path = f"{path}.{k}" if path else k
            if k in bad_keys:
                issues.append(QuarantineValidationIssue("error", current_path, f"Contains broker field: {k}"))
            if isinstance(v, dict):
                _check(v, current_path)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                         _check(item, f"{current_path}[{i}]")

    _check(payload)
    return issues

def _check_paper_mutation_fields(payload: dict[str, Any]) -> list[QuarantineValidationIssue]:
    issues = []
    bad_keys = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]

    def _check(d: dict, path: str = ""):
        for k, v in d.items():
            current_path = f"{path}.{k}" if path else k
            if k in bad_keys and v is True:
                issues.append(QuarantineValidationIssue("error", current_path, f"Contains active paper mutation field: {k}=True"))
            if isinstance(v, dict):
                _check(v, current_path)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                         _check(item, f"{current_path}[{i}]")

    _check(payload)
    return issues

def _check_live_language(text: str) -> list[QuarantineValidationIssue]:
    issues = []
    text_lower = text.lower()
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]

    for p in bad_phrases:
        if p in text_lower:
            issues.append(QuarantineValidationIssue("error", "text", f"Contains disallowed live execution language: '{p}'"))

    return issues

def validate_no_sensitive_data_in_quarantine_payload(payload: dict[str, Any]) -> QuarantineValidationReport:
    # Use existing redaction logic to find if secrets exist
    from usa_signal_bot.paper_quarantine.paper_snapshot_ref import redact_snapshot_sensitive_fields
    redacted = redact_snapshot_sensitive_fields(payload)

    issues = []
    # simplified check - if it changed, it had a secret
    if json.dumps(payload, sort_keys=True) != json.dumps(redacted, sort_keys=True):
        issues.append(QuarantineValidationIssue("error", None, "Contains unredacted sensitive data"))

    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_broker_execution_fields_in_quarantine(payload: dict[str, Any]) -> QuarantineValidationReport:
    issues = _check_broker_fields(payload)
    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_paper_state_mutation_fields_in_quarantine(payload: dict[str, Any]) -> QuarantineValidationReport:
    issues = _check_paper_mutation_fields(payload)
    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_live_execution_language_in_quarantine(text: str) -> QuarantineValidationReport:
    issues = _check_live_language(text)
    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_real_order_language_in_quarantine(text: str) -> QuarantineValidationReport:
    return validate_no_live_execution_language_in_quarantine(text)

def validate_quarantined_candidate_report(item: QuarantinedPaperCandidate) -> QuarantineValidationReport:
    issues = []
    if item.allowed_for_active_paper:
         issues.append(QuarantineValidationIssue("error", "allowed_for_active_paper", "Must be False"))
    if item.allowed_for_broker_execution:
         issues.append(QuarantineValidationIssue("error", "allowed_for_broker_execution", "Must be False"))

    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_promotion_ticket_report(item: ReadOnlyPromotionTicket) -> QuarantineValidationReport:
    issues = []
    if not item.read_only:
         issues.append(QuarantineValidationIssue("error", "read_only", "Must be True"))
    if item.allowed_for_active_paper:
         issues.append(QuarantineValidationIssue("error", "allowed_for_active_paper", "Must be False"))
    if item.allowed_for_broker_execution:
         issues.append(QuarantineValidationIssue("error", "allowed_for_broker_execution", "Must be False"))
    if item.allowed_for_config_patch:
         issues.append(QuarantineValidationIssue("error", "allowed_for_config_patch", "Must be False"))

    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_bridge_plan_report(item: SupervisedDryRunBridgePlan) -> QuarantineValidationReport:
    issues = []
    if item.bridge_execution_enabled:
        issues.append(QuarantineValidationIssue("error", "bridge_execution_enabled", "Must be False"))
    if item.paper_state_mutation_enabled:
        issues.append(QuarantineValidationIssue("error", "paper_state_mutation_enabled", "Must be False"))
    if item.paper_order_enabled:
        issues.append(QuarantineValidationIssue("error", "paper_order_enabled", "Must be False"))
    if item.broker_order_enabled:
        issues.append(QuarantineValidationIssue("error", "broker_order_enabled", "Must be False"))
    if item.telegram_real_send_enabled:
        issues.append(QuarantineValidationIssue("error", "telegram_real_send_enabled", "Must be False"))
    if item.production_config_write_enabled:
        issues.append(QuarantineValidationIssue("error", "production_config_write_enabled", "Must be False"))

    forbidden = [
        BridgeOperation.WRITE_PAPER_STATE,
        BridgeOperation.SEND_PAPER_ORDER,
        BridgeOperation.SEND_BROKER_ORDER,
        BridgeOperation.SEND_TELEGRAM_REAL,
        BridgeOperation.WRITE_PRODUCTION_CONFIG,
    ]
    for op in forbidden:
        if op in item.allowed_operations:
             issues.append(QuarantineValidationIssue("error", "allowed_operations", f"Forbidden operation {op.value} allowed"))

    return QuarantineValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_quarantine_review_report(item: QuarantineEnrollmentReview) -> QuarantineValidationReport:
    from usa_signal_bot.paper_quarantine.quarantine_models import quarantine_enrollment_review_to_dict
    payload = quarantine_enrollment_review_to_dict(item)

    all_issues = []

    broker_rep = validate_no_broker_execution_fields_in_quarantine(payload)
    all_issues.extend(broker_rep.issues)

    mutation_rep = validate_no_paper_state_mutation_fields_in_quarantine(payload)
    all_issues.extend(mutation_rep.issues)

    secret_rep = validate_no_sensitive_data_in_quarantine_payload(payload)
    all_issues.extend(secret_rep.issues)

    text = json.dumps(payload)
    lang_rep = validate_no_live_execution_language_in_quarantine(text)
    all_issues.extend(lang_rep.issues)

    for c in item.candidates:
        r = validate_quarantined_candidate_report(c)
        all_issues.extend(r.issues)
    for t in item.tickets:
        r = validate_promotion_ticket_report(t)
        all_issues.extend(r.issues)
    for p in item.bridge_plans:
        r = validate_bridge_plan_report(p)
        all_issues.extend(r.issues)

    return QuarantineValidationReport(
        valid=len(all_issues) == 0,
        issue_count=len(all_issues),
        warning_count=0,
        error_count=len(all_issues),
        blocked_count=len(all_issues),
        issues=all_issues,
        warnings=[],
        errors=[i.message for i in all_issues]
    )

def quarantine_validation_report_to_text(report: QuarantineValidationReport) -> str:
    lines = [
        f"Validation Report: {'VALID' if report.valid else 'INVALID'}",
        f"Errors: {report.error_count}",
        "-" * 20
    ]
    for issue in report.issues:
        lines.append(f"[{issue.severity.upper()}] {issue.field or 'General'}: {issue.message}")
    return "\n".join(lines)

def assert_quarantine_valid(report: QuarantineValidationReport) -> None:
    if not report.valid:
        raise QuarantineValidationError(f"Quarantine validation failed: {[i.message for i in report.issues]}")
