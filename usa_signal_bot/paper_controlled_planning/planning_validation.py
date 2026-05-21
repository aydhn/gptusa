import re
from typing import Any, List, Optional
from dataclasses import dataclass, field
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket,
    PaperAdjacentRehearsalRun,
    FinalHumanApprovalQueueItem,
    ControlledPlanningReview
)
from usa_signal_bot.core.exceptions import ControlledPlanningValidationError

@dataclass
class ControlledPlanningValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ControlledPlanningValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ControlledPlanningValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_controlled_planning_ticket_report(item: ControlledPlanningTicket) -> ControlledPlanningValidationReport:
    issues = []
    if item.allowed_for_active_paper:
        issues.append(ControlledPlanningValidationIssue("ERROR", "allowed_for_active_paper", "Must be false"))
    if item.allowed_for_broker_execution:
        issues.append(ControlledPlanningValidationIssue("ERROR", "allowed_for_broker_execution", "Must be false"))
    if item.allowed_for_paper_state_mutation:
        issues.append(ControlledPlanningValidationIssue("ERROR", "allowed_for_paper_state_mutation", "Must be false"))
    if item.allowed_for_config_patch:
        issues.append(ControlledPlanningValidationIssue("ERROR", "allowed_for_config_patch", "Must be false"))
    return _build_validation_report(issues)

def validate_adjacent_rehearsal_run_report(item: PaperAdjacentRehearsalRun) -> ControlledPlanningValidationReport:
    issues = []
    if item.context:
        if item.context.allow_active_paper:
            issues.append(ControlledPlanningValidationIssue("ERROR", "allow_active_paper", "Must be false"))
        if item.context.allow_paper_orders:
            issues.append(ControlledPlanningValidationIssue("ERROR", "allow_paper_orders", "Must be false"))
        if item.context.allow_broker_orders:
            issues.append(ControlledPlanningValidationIssue("ERROR", "allow_broker_orders", "Must be false"))
    for p in item.proposals:
        if p.is_real_order:
            issues.append(ControlledPlanningValidationIssue("ERROR", "is_real_order", f"Proposal {p.proposal_id} is real order"))
        if p.will_mutate_paper_state:
            issues.append(ControlledPlanningValidationIssue("ERROR", "will_mutate_paper_state", f"Proposal {p.proposal_id} mutates state"))
    return _build_validation_report(issues)

def validate_approval_queue_item_report(item: FinalHumanApprovalQueueItem) -> ControlledPlanningValidationReport:
    issues = []
    if item.allows_active_paper:
        issues.append(ControlledPlanningValidationIssue("ERROR", "allows_active_paper", "Must be false"))
    if item.allows_broker_execution:
        issues.append(ControlledPlanningValidationIssue("ERROR", "allows_broker_execution", "Must be false"))
    return _build_validation_report(issues)

def validate_controlled_planning_review_report(item: ControlledPlanningReview) -> ControlledPlanningValidationReport:
    issues = []
    for t in item.planning_tickets:
        rep = validate_controlled_planning_ticket_report(t)
        issues.extend(rep.issues)
    for r in item.rehearsal_runs:
        rep = validate_adjacent_rehearsal_run_report(r)
        issues.extend(rep.issues)
    for q in item.approval_queue_items:
        rep = validate_approval_queue_item_report(q)
        issues.extend(rep.issues)
    return _build_validation_report(issues)

def validate_no_sensitive_data_in_controlled_planning_payload(payload: dict[str, Any]) -> ControlledPlanningValidationReport:
    issues = []
    import json
    text = json.dumps(payload).lower()
    for secret_key in ["api_key", "secret", "token", "password", "alpaca_key", "telegram_token"]:
        if secret_key in text:
            issues.append(ControlledPlanningValidationIssue("ERROR", None, f"Sensitive data key found: {secret_key}"))
    return _build_validation_report(issues)

def validate_no_live_execution_language_in_controlled_planning(text: str) -> ControlledPlanningValidationReport:
    issues = []
    lower_text = text.lower()
    blocked_terms = ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir"]
    for term in blocked_terms:
        if term in lower_text:
            issues.append(ControlledPlanningValidationIssue("ERROR", None, f"Live execution language found: {term}"))
    return _build_validation_report(issues)

def validate_no_active_paper_language_in_controlled_planning(text: str) -> ControlledPlanningValidationReport:
    issues = []
    lower_text = text.lower()
    blocked_terms = ["paper'a uygula", "canlıya al", "aktif et", "kesin kâr", "candidate kesin iyi"]
    for term in blocked_terms:
        if term in lower_text:
            issues.append(ControlledPlanningValidationIssue("ERROR", None, f"Active paper language found: {term}"))
    return _build_validation_report(issues)

def validate_no_paper_state_mutation_fields_in_controlled_planning(payload: dict[str, Any]) -> ControlledPlanningValidationReport:
    issues = []
    import json
    text = json.dumps(payload)
    if "paper_state_committed\": true" in text.lower():
        issues.append(ControlledPlanningValidationIssue("ERROR", "paper_state_committed", "Found True"))
    if "paper_order_executed\": true" in text.lower():
        issues.append(ControlledPlanningValidationIssue("ERROR", "paper_order_executed", "Found True"))
    if "portfolio_state_mutated\": true" in text.lower():
        issues.append(ControlledPlanningValidationIssue("ERROR", "portfolio_state_mutated", "Found True"))
    return _build_validation_report(issues)

def validate_no_broker_execution_fields_in_controlled_planning(payload: dict[str, Any]) -> ControlledPlanningValidationReport:
    issues = []
    import json
    text = json.dumps(payload)
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if field in text:
            issues.append(ControlledPlanningValidationIssue("ERROR", field, f"Found restricted field: {field}"))
    return _build_validation_report(issues)

def _build_validation_report(issues: List[ControlledPlanningValidationIssue]) -> ControlledPlanningValidationReport:
    errs = [i for i in issues if i.severity == "ERROR"]
    warns = [i for i in issues if i.severity == "WARNING"]
    blocks = [i for i in issues if i.severity == "BLOCKED"]
    return ControlledPlanningValidationReport(
        valid=len(errs) == 0 and len(blocks) == 0,
        issue_count=len(issues),
        warning_count=len(warns),
        error_count=len(errs),
        blocked_count=len(blocks),
        issues=issues,
        warnings=[i.message for i in warns],
        errors=[i.message for i in errs]
    )

def assert_controlled_planning_valid(report: ControlledPlanningValidationReport) -> None:
    if not report.valid:
        raise ControlledPlanningValidationError(f"Controlled planning validation failed: {report.errors}")

def controlled_planning_validation_report_to_text(report: ControlledPlanningValidationReport) -> str:
    lines = [
        "🛡️ CONTROLLED PLANNING VALIDATION REPORT",
        f"Valid: {report.valid}",
        f"Issues: {report.issue_count} (E: {report.error_count}, W: {report.warning_count}, B: {report.blocked_count})"
    ]
    if report.errors:
        lines.append("ERRORS:")
        for e in report.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
