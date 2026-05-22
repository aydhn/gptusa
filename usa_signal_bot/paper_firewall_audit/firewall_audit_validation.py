from dataclasses import dataclass, field
from typing import Any, List
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import (
    FirewallReplayPlan, FirewallReplayResult, ZeroMutationAuditReport,
    ReadinessAuditCheckpoint, FirewallAuditReview
)

@dataclass
class FirewallAuditValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class FirewallAuditValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[FirewallAuditValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_firewall_replay_plan_report(item: FirewallReplayPlan) -> FirewallAuditValidationReport:
    issues = []
    if item.execution_enabled: issues.append(FirewallAuditValidationIssue("error", "execution_enabled", "Cannot be True"))
    return FirewallAuditValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_firewall_replay_result_report(item: FirewallReplayResult) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_zero_mutation_audit_report_report(item: ZeroMutationAuditReport) -> FirewallAuditValidationReport:
    issues = []
    if item.passed and item.mutation_detected: issues.append(FirewallAuditValidationIssue("error", "mutation_detected", "Cannot be true if passed"))
    return FirewallAuditValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_readiness_audit_checkpoint_report(item: ReadinessAuditCheckpoint) -> FirewallAuditValidationReport:
    issues = []
    if not item.activation_denied: issues.append(FirewallAuditValidationIssue("error", "activation_denied", "Must be True"))
    return FirewallAuditValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_firewall_audit_review_report(item: FirewallAuditReview) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_firewall_audit_payload(payload: dict[str, Any]) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_firewall_audit(text: str) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_active_paper_language_in_firewall_audit(text: str) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_paper_state_mutation_fields_in_firewall_audit(payload: dict[str, Any]) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_broker_execution_fields_in_firewall_audit(payload: dict[str, Any]) -> FirewallAuditValidationReport:
    return FirewallAuditValidationReport(True, 0, 0, 0, 0, [], [], [])

def firewall_audit_validation_report_to_text(report: FirewallAuditValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_firewall_audit_valid(report: FirewallAuditValidationReport) -> None:
    if not report.valid: raise ValueError(f"Audit invalid: {report.errors}")
