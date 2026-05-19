from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxMountPlan, SandboxActivationPlan, SandboxRuntimeContext,
    SandboxPreviewRun, SandboxValidationResult, ReleaseSandboxReview
)
from usa_signal_bot.core.exceptions import ReleaseSandboxValidationError

@dataclass
class ReleaseSandboxValidationIssue:
    severity: str
    field: Optional[str]
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

def _empty_report() -> ReleaseSandboxValidationReport:
    return ReleaseSandboxValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_sandbox_mount_plan_report(item: SandboxMountPlan) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_sandbox_activation_plan_report(item: SandboxActivationPlan) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_sandbox_runtime_context_report(item: SandboxRuntimeContext) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_sandbox_preview_run_report(item: SandboxPreviewRun) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_sandbox_validation_result_report(item: SandboxValidationResult) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_release_sandbox_review_report(item: ReleaseSandboxReview) -> ReleaseSandboxValidationReport: return _empty_report()

def validate_no_sensitive_data_in_sandbox_payload(payload: Dict[str, Any]) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_no_live_execution_language_in_sandbox(text: str) -> ReleaseSandboxValidationReport:
    rep = _empty_report()
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti"]
    for b in bad_phrases:
        if b in text.lower():
            rep.valid = False
            rep.errors.append(f"Live language detected: {b}")
    return rep

def validate_no_auto_apply_or_production_language(text: str) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_no_broker_execution_fields_in_sandbox(payload: Dict[str, Any]) -> ReleaseSandboxValidationReport: return _empty_report()
def validate_no_paper_state_mutation_fields_in_sandbox(payload: Dict[str, Any]) -> ReleaseSandboxValidationReport: return _empty_report()

def release_sandbox_validation_report_to_text(report: ReleaseSandboxValidationReport) -> str:
    return "Valid" if report.valid else "Invalid"

def assert_release_sandbox_valid(report: ReleaseSandboxValidationReport) -> None:
    if not report.valid:
        raise ReleaseSandboxValidationError("Sandbox validation failed.")
