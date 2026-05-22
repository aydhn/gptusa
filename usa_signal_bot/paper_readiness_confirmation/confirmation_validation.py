from typing import Any
from dataclasses import dataclass, field
import json

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    ActivationStillDeniedRegistryEntry,
    ReadinessConfirmationReview
)

@dataclass
class ReadinessConfirmationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessConfirmationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ReadinessConfirmationValidationIssue]
    warnings: list[str]
    errors: list[str]

def _build_report(issues: list[ReadinessConfirmationValidationIssue]) -> ReadinessConfirmationValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocks = [i.message for i in issues if i.severity == "BLOCK"]
    return ReadinessConfirmationValidationReport(
        valid=len(errors) == 0 and len(blocks) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocks),
        issues=issues,
        warnings=warnings,
        errors=errors + blocks
    )

def validate_confirmation_queue_item_report(item: ReadinessConfirmationQueueItem) -> ReadinessConfirmationValidationReport:
    issues = []
    if not item.activation_denied_required:
         issues.append(ReadinessConfirmationValidationIssue("ERROR", "activation_denied_required", "Must be True"))
    if not item.manual_review_required:
         issues.append(ReadinessConfirmationValidationIssue("WARNING", "manual_review_required", "Should be True"))
    if item.allows_active_paper:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", "allows_active_paper", "Must be False"))
    if item.allows_broker_execution:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", "allows_broker_execution", "Must be False"))
    return _build_report(issues)

def validate_human_review_bundle_report(item: HumanReviewBundle) -> ReadinessConfirmationValidationReport:
    issues = []
    if not item.activation_denied:
         issues.append(ReadinessConfirmationValidationIssue("ERROR", "activation_denied", "Must be True"))
    if item.activation_allowed:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", "activation_allowed", "Must be False"))
    if item.allows_active_paper:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", "allows_active_paper", "Must be False"))
    return _build_report(issues)

def validate_activation_denied_registry_entry_report(item: ActivationStillDeniedRegistryEntry) -> ReadinessConfirmationValidationReport:
    issues = []
    if not item.activation_denied:
         issues.append(ReadinessConfirmationValidationIssue("ERROR", "activation_denied", "Must be True"))
    if item.activation_allowed:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", "activation_allowed", "Must be False"))
    if item.allows_active_paper:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", "allows_active_paper", "Must be False"))
    return _build_report(issues)

def validate_readiness_confirmation_review_report(item: ReadinessConfirmationReview) -> ReadinessConfirmationValidationReport:
    issues = []
    for q in item.queue_items:
         r = validate_confirmation_queue_item_report(q)
         issues.extend(r.issues)
    for b in item.bundles:
         r = validate_human_review_bundle_report(b)
         issues.extend(r.issues)
    for e in item.registry_entries:
         r = validate_activation_denied_registry_entry_report(e)
         issues.extend(r.issues)

    text = json.dumps({
        "warnings": item.warnings,
        "errors": item.errors
    })
    r_lang = validate_no_live_execution_language_in_confirmation(text)
    issues.extend(r_lang.issues)

    return _build_report(issues)

def validate_no_sensitive_data_in_confirmation_payload(payload: dict[str, Any]) -> ReadinessConfirmationValidationReport:
    text = json.dumps(payload).lower()
    issues = []
    if "api_key" in text or "secret" in text or "token" in text:
         issues.append(ReadinessConfirmationValidationIssue("BLOCK", None, "Token/secret leak risk detected."))
    return _build_report(issues)

def validate_no_live_execution_language_in_confirmation(text: str) -> ReadinessConfirmationValidationReport:
    issues = []
    t = text.lower()
    banned = ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir", "kesin kâr", "candidate kesin iyi"]
    for b in banned:
        if b in t:
             issues.append(ReadinessConfirmationValidationIssue("BLOCK", None, f"Live execution language detected: {b}"))
    return _build_report(issues)

def validate_no_active_paper_language_in_confirmation(text: str) -> ReadinessConfirmationValidationReport:
    issues = []
    t = text.lower()
    banned = ["paper'a uygula", "canlıya al", "aktif et"]
    for b in banned:
        if b in t:
             issues.append(ReadinessConfirmationValidationIssue("BLOCK", None, f"Active paper language detected: {b}"))
    return _build_report(issues)

def validate_no_paper_state_mutation_fields_in_confirmation(payload: dict[str, Any]) -> ReadinessConfirmationValidationReport:
    issues = []
    text = json.dumps(payload)
    banned = [
        "paper_state_committed", "paper_order_executed", "portfolio_state_mutated",
        "position_mutated", "cash_mutated", "equity_mutated"
    ]
    for b in banned:
        if f'"{b}"' in text:
             issues.append(ReadinessConfirmationValidationIssue("BLOCK", b, f"Paper state mutation field detected: {b}"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_confirmation(payload: dict[str, Any]) -> ReadinessConfirmationValidationReport:
    issues = []
    text = json.dumps(payload)
    banned = [
        "broker_order_id", "live_order_id", "sent_to_broker",
        "execution_venue", "real_fill_id"
    ]
    for b in banned:
        if f'"{b}"' in text:
             issues.append(ReadinessConfirmationValidationIssue("BLOCK", b, f"Broker execution field detected: {b}"))
    return _build_report(issues)

def readiness_confirmation_validation_report_to_text(report: ReadinessConfirmationValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}, Blocks: {report.blocked_count}"

def assert_readiness_confirmation_valid(report: ReadinessConfirmationValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Readiness confirmation validation failed: {report.errors}")
