from dataclasses import dataclass, field
from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import (
    GovernanceEvidencePack, PromotionReview, ReleaseCandidatePackage,
    DecisionBoardResult, GovernanceReview
)
from usa_signal_bot.core.exceptions import GovernanceValidationError
import json

@dataclass
class GovernanceValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class GovernanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[GovernanceValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_evidence_pack_report(item: GovernanceEvidencePack) -> GovernanceValidationReport:
    return GovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_promotion_review_report(item: PromotionReview) -> GovernanceValidationReport:
    issues = []
    if item.allowed_for_auto_promotion: issues.append(GovernanceValidationIssue("ERROR", "allowed_for_auto_promotion", "Must be False"))
    if item.allowed_for_config_patch: issues.append(GovernanceValidationIssue("ERROR", "allowed_for_config_patch", "Must be False"))
    if item.allowed_for_order_routing: issues.append(GovernanceValidationIssue("ERROR", "allowed_for_order_routing", "Must be False"))
    valid = len(issues) == 0
    return GovernanceValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_release_candidate_report(item: ReleaseCandidatePackage) -> GovernanceValidationReport:
    issues = []
    if item.allowed_for_auto_apply: issues.append(GovernanceValidationIssue("ERROR", "allowed_for_auto_apply", "Must be False"))
    if item.allowed_for_live_or_demo_execution: issues.append(GovernanceValidationIssue("ERROR", "allowed_for_live_or_demo_execution", "Must be False"))
    valid = len(issues) == 0
    return GovernanceValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_decision_board_result_report(item: DecisionBoardResult) -> GovernanceValidationReport:
    return GovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_governance_review_report(item: GovernanceReview) -> GovernanceValidationReport:
    return GovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_governance_payload(payload: dict[str, Any]) -> GovernanceValidationReport:
    txt = json.dumps(payload).lower()
    issues = []
    if "api_key" in txt or "secret" in txt or "token" in txt:
        # Extremely basic check for demo purposes
        issues.append(GovernanceValidationIssue("ERROR", None, "Potential secret leak in payload"))
    valid = len(issues) == 0
    return GovernanceValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_live_execution_language_in_governance(text: str) -> GovernanceValidationReport:
    issues = []
    t = text.lower()
    for w in ["live approved", "sent to broker", "kesin al", "garanti"]:
        if w in t:
            issues.append(GovernanceValidationIssue("ERROR", None, f"Found live execution language: {w}"))
    valid = len(issues) == 0
    return GovernanceValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_auto_apply_or_production_language(text: str) -> GovernanceValidationReport:
    issues = []
    t = text.lower()
    for w in ["production'a gecir", "otomatik uygula", "canliya al", "kesin kar", "candidate kesin iyi", "production'a geçir", "kesin kâr", "canlıya al"]:
        if w in t:
            issues.append(GovernanceValidationIssue("ERROR", None, f"Found auto-apply language: {w}"))
    valid = len(issues) == 0
    return GovernanceValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_broker_execution_fields_in_governance(payload: dict[str, Any]) -> GovernanceValidationReport:
    txt = json.dumps(payload).lower()
    issues = []
    for w in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if w in txt:
            issues.append(GovernanceValidationIssue("ERROR", None, f"Found broker field: {w}"))
    valid = len(issues) == 0
    return GovernanceValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def governance_validation_report_to_text(report: GovernanceValidationReport) -> str:
    return f"Governance Validation: {'Valid' if report.valid else 'Invalid'}"

def assert_governance_valid(report: GovernanceValidationReport) -> None:
    if not report.valid:
        raise GovernanceValidationError(f"Governance validation failed: {report.errors}")
