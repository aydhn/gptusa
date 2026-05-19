from dataclasses import dataclass, field
from typing import Any, Dict, List
import json
from usa_signal_bot.core.exceptions import ReleaseSandboxValidationError
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxMountPlan, SandboxActivationPlan, SandboxRuntimeContext,
    SandboxPreviewRun, SandboxValidationResult, ReleaseSandboxReview
)

@dataclass
class ReleaseSandboxValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleaseSandboxValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ReleaseSandboxValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_sandbox_mount_plan_report(item: SandboxMountPlan) -> ReleaseSandboxValidationReport:
    issues = []
    return ReleaseSandboxValidationReport(True, len(issues), 0, 0, 0, issues, [], [])

def validate_sandbox_activation_plan_report(item: SandboxActivationPlan) -> ReleaseSandboxValidationReport:
    issues = []
    if getattr(item, "allowed_for_production_apply", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_for_production_apply", "Must be False."))
    if getattr(item, "allowed_for_order_routing", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_for_order_routing", "Must be False."))
    if getattr(item, "allowed_for_paper_state_mutation", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_for_paper_state_mutation", "Must be False."))

    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_sandbox_runtime_context_report(item: SandboxRuntimeContext) -> ReleaseSandboxValidationReport:
    issues = []
    if getattr(item, "allowed_to_write_production_config", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_to_write_production_config", "Must be False."))
    if getattr(item, "allowed_to_mutate_paper_state", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_to_mutate_paper_state", "Must be False."))
    if getattr(item, "allowed_to_send_orders", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_to_send_orders", "Must be False."))
    if getattr(item, "allowed_to_send_telegram_real", False):
         issues.append(ReleaseSandboxValidationIssue("ERROR", "allowed_to_send_telegram_real", "Must be False."))
    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_sandbox_preview_run_report(item: SandboxPreviewRun) -> ReleaseSandboxValidationReport:
    return ReleaseSandboxValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_sandbox_validation_result_report(item: SandboxValidationResult) -> ReleaseSandboxValidationReport:
    return ReleaseSandboxValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_release_sandbox_review_report(item: ReleaseSandboxReview) -> ReleaseSandboxValidationReport:
    return ReleaseSandboxValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_sandbox_payload(payload: Dict[str, Any]) -> ReleaseSandboxValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    if "api_key" in payload_str or "secret" in payload_str or "token" in payload_str:
        issues.append(ReleaseSandboxValidationIssue("ERROR", None, "Secret/token leak risk detected."))
    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_live_execution_language_in_sandbox(text: str) -> ReleaseSandboxValidationReport:
    issues = []
    text_lower = text.lower()
    bad_terms = ["live approved", "sent to broker", "kesin al", "garanti", "kesin kâr"]
    for term in bad_terms:
        if term in text_lower:
            issues.append(ReleaseSandboxValidationIssue("ERROR", None, f"Live execution language found: '{term}'"))
    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_auto_apply_or_production_language(text: str) -> ReleaseSandboxValidationReport:
    issues = []
    text_lower = text.lower()
    bad_terms = ["production'a geçir", "otomatik uygula", "canlıya al", "paper'a uygula", "candidate kesin iyi"]
    for term in bad_terms:
        if term in text_lower:
            issues.append(ReleaseSandboxValidationIssue("ERROR", None, f"Auto-apply language found: '{term}'"))
    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_broker_execution_fields_in_sandbox(payload: Dict[str, Any]) -> ReleaseSandboxValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    bad_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for field in bad_fields:
        if field in payload_str:
            issues.append(ReleaseSandboxValidationIssue("ERROR", field, f"Broker field '{field}' detected."))
    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_paper_state_mutation_fields_in_sandbox(payload: Dict[str, Any]) -> ReleaseSandboxValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    bad_fields = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]
    for field in bad_fields:
        if field in payload_str:
            issues.append(ReleaseSandboxValidationIssue("ERROR", field, f"Paper mutation field '{field}' detected."))
    return ReleaseSandboxValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def release_sandbox_validation_report_to_text(report: ReleaseSandboxValidationReport) -> str:
    return f"Sandbox Validation Report: Valid={report.valid}, Issues={report.issue_count}"

def assert_release_sandbox_valid(report: ReleaseSandboxValidationReport) -> None:
    if not report.valid:
        msg = ", ".join(report.errors)
        raise ReleaseSandboxValidationError(f"Sandbox Validation failed: {msg}")
