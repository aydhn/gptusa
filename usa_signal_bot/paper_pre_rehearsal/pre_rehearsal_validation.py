from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalPlan,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    PrePaperDryRehearsalReview
)
from usa_signal_bot.core.exceptions import PrePaperValidationError

@dataclass
class PrePaperValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PrePaperValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[PrePaperValidationIssue]) -> PrePaperValidationReport:
    errors = [i for i in issues if i.severity == "ERROR"]
    blocks = [i for i in issues if i.severity == "BLOCK"]
    warnings = [i for i in issues if i.severity == "WARNING"]

    return PrePaperValidationReport(
        valid=len(errors) == 0 and len(blocks) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocks),
        issues=issues,
        warnings=[w.message for w in warnings],
        errors=[e.message for e in errors] + [b.message for b in blocks]
    )

def validate_pre_paper_plan_report(item: PrePaperDryRehearsalPlan) -> PrePaperValidationReport:
    issues = []
    if item.execution_enabled: issues.append(PrePaperValidationIssue("BLOCK", "execution_enabled", "Must be false"))
    if item.active_paper_enabled: issues.append(PrePaperValidationIssue("BLOCK", "active_paper_enabled", "Must be false"))
    if item.broker_execution_enabled: issues.append(PrePaperValidationIssue("BLOCK", "broker_execution_enabled", "Must be false"))
    if item.paper_state_mutation_enabled: issues.append(PrePaperValidationIssue("BLOCK", "paper_state_mutation_enabled", "Must be false"))
    if item.config_patch_enabled: issues.append(PrePaperValidationIssue("BLOCK", "config_patch_enabled", "Must be false"))
    if item.telegram_real_send_enabled: issues.append(PrePaperValidationIssue("BLOCK", "telegram_real_send_enabled", "Must be false"))
    if not item.firewall_required: issues.append(PrePaperValidationIssue("ERROR", "firewall_required", "Must be true"))
    if not item.activation_denied_required: issues.append(PrePaperValidationIssue("ERROR", "activation_denied_required", "Must be true"))
    return _create_report(issues)

def validate_pre_paper_run_report(item: PrePaperDryRehearsalRun) -> PrePaperValidationReport:
    issues = []
    if item.plan:
        pr = validate_pre_paper_plan_report(item.plan)
        issues.extend(pr.issues)
    if len(item.firewall_rules) == 0:
        issues.append(PrePaperValidationIssue("ERROR", "firewall_rules", "No firewall rules present"))
    return _create_report(issues)

def validate_activation_checkpoint_report(item: ActivationDeniedCheckpoint) -> PrePaperValidationReport:
    issues = []
    if not item.activation_denied: issues.append(PrePaperValidationIssue("BLOCK", "activation_denied", "Must be true"))
    if item.allows_active_paper: issues.append(PrePaperValidationIssue("BLOCK", "allows_active_paper", "Must be false"))
    if item.allows_broker_execution: issues.append(PrePaperValidationIssue("BLOCK", "allows_broker_execution", "Must be false"))
    if item.allows_paper_state_mutation: issues.append(PrePaperValidationIssue("BLOCK", "allows_paper_state_mutation", "Must be false"))
    if item.allows_config_patch: issues.append(PrePaperValidationIssue("BLOCK", "allows_config_patch", "Must be false"))
    if item.allows_telegram_real_send: issues.append(PrePaperValidationIssue("BLOCK", "allows_telegram_real_send", "Must be false"))
    return _create_report(issues)

def validate_pre_paper_review_report(item: PrePaperDryRehearsalReview) -> PrePaperValidationReport:
    issues = []
    for plan in item.plans:
        issues.extend(validate_pre_paper_plan_report(plan).issues)
    for run in item.runs:
        issues.extend(validate_pre_paper_run_report(run).issues)
    for cp in item.activation_checkpoints:
        issues.extend(validate_activation_checkpoint_report(cp).issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_pre_paper_payload(payload: Dict[str, Any]) -> PrePaperValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    for secret in ["api_key", "secret", "token", "password"]:
        if f'"{secret}"' in payload_str and "[redacted]" not in payload_str:
            issues.append(PrePaperValidationIssue("BLOCK", None, f"Potential sensitive data leak: {secret}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_pre_paper(text: str) -> PrePaperValidationReport:
    issues = []
    t = text.lower()
    for phrase in ["sent to broker", "live approved", "gerçek emir", "kesin al", "garanti"]:
        if phrase in t:
            issues.append(PrePaperValidationIssue("BLOCK", None, f"Live execution language detected: {phrase}"))
    return _create_report(issues)

def validate_no_active_paper_language_in_pre_paper(text: str) -> PrePaperValidationReport:
    issues = []
    t = text.lower()
    for phrase in ["paper'a uygula", "canlıya al", "aktif et"]:
        if phrase in t:
            issues.append(PrePaperValidationIssue("BLOCK", None, f"Active paper language detected: {phrase}"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_pre_paper(payload: Dict[str, Any]) -> PrePaperValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    for field in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if f'"{field}": true' in payload_str or f'"{field}":true' in payload_str:
            issues.append(PrePaperValidationIssue("BLOCK", field, f"Paper state mutation field set to true: {field}"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_pre_paper(payload: Dict[str, Any]) -> PrePaperValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f'"{field}"' in payload_str and "null" not in payload_str and "none" not in payload_str:
             # Just a simple heuristic; it shouldn't contain these keys with values
             issues.append(PrePaperValidationIssue("BLOCK", field, f"Broker execution field detected: {field}"))
    return _create_report(issues)

def pre_paper_validation_report_to_text(report: PrePaperValidationReport) -> str:
    return f"Pre-Paper Validation: Valid={report.valid}, Errors={report.error_count}, Blocks={report.blocked_count}, Warnings={report.warning_count}"

def assert_pre_paper_valid(report: PrePaperValidationReport) -> None:
    if not report.valid:
        raise PrePaperValidationError(f"Validation failed: {pre_paper_validation_report_to_text(report)}")
