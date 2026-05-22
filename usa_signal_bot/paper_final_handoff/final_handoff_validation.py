from dataclasses import dataclass, field
from typing import Any, Dict, List
import re
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    PrePaperGovernanceCheckpoint,
    FinalHandoffFullReview
)
from usa_signal_bot.core.exceptions import FinalHandoffValidationError

@dataclass
class FinalHandoffValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalHandoffValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[FinalHandoffValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_final_handoff_review_report(item: FinalHandoffReview) -> FinalHandoffValidationReport:
    issues = []
    if item.allows_active_paper: issues.append(FinalHandoffValidationIssue("error", "allows_active_paper", "Cannot allow active paper."))
    if item.allows_broker_execution: issues.append(FinalHandoffValidationIssue("error", "allows_broker_execution", "Cannot allow broker execution."))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def validate_archive_manifest_report(item: SealedReadinessArchiveManifest) -> FinalHandoffValidationReport:
    issues = []
    if item.sealed and not item.immutable: issues.append(FinalHandoffValidationIssue("error", "immutable", "Sealed manifest must be immutable."))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def validate_pre_paper_checkpoint_report(item: PrePaperGovernanceCheckpoint) -> FinalHandoffValidationReport:
    return FinalHandoffValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_final_handoff_full_review_report(item: FinalHandoffFullReview) -> FinalHandoffValidationReport:
    return FinalHandoffValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_final_handoff_payload(payload: Dict[str, Any]) -> FinalHandoffValidationReport:
    s = str(payload)
    issues = []
    if "api_key" in s.lower() or "secret" in s.lower():
        issues.append(FinalHandoffValidationIssue("error", "payload", "Found sensitive data terms."))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def validate_no_live_execution_language_in_final_handoff(text: str) -> FinalHandoffValidationReport:
    issues = []
    if re.search(r"live approved|sent to broker|kesin al|garanti|gerçek emir", text, re.IGNORECASE):
        issues.append(FinalHandoffValidationIssue("error", "text", "Found live execution language."))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def validate_no_active_paper_language_in_final_handoff(text: str) -> FinalHandoffValidationReport:
    issues = []
    if re.search(r"paper'a uygula|canlıya al|aktif et|kesin kâr|candidate kesin iyi", text, re.IGNORECASE):
        issues.append(FinalHandoffValidationIssue("error", "text", "Found active paper/advice language."))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def validate_no_paper_state_mutation_fields_in_final_handoff(payload: Dict[str, Any]) -> FinalHandoffValidationReport:
    s = str(payload)
    issues = []
    if "paper_state_committed" in s or "portfolio_state_mutated" in s:
        issues.append(FinalHandoffValidationIssue("error", "payload", "Found paper state mutation fields."))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def validate_no_broker_execution_fields_in_final_handoff(payload: Dict[str, Any]) -> FinalHandoffValidationReport:
    s = str(payload)
    issues = []
    for f in ["broker_order_id", "live_order_id", "execution_venue", "real_fill_id"]:
        if f in s: issues.append(FinalHandoffValidationIssue("error", "payload", f"Found broker field: {f}"))
    return FinalHandoffValidationReport(len(issues) == 0, len(issues), 0, len(issues), 0, issues, [], [])

def final_handoff_validation_report_to_text(report: FinalHandoffValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_final_handoff_valid(report: FinalHandoffValidationReport) -> None:
    if not report.valid:
        raise FinalHandoffValidationError("Final handoff validation failed.")
