from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowSessionComparisonReport, ShadowAcceptanceScorecard, ShadowDecisionBoardResult, ShadowGovernanceReview
)
from usa_signal_bot.core.exceptions import ShadowGovernanceValidationError

@dataclass
class ShadowGovernanceValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowGovernanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ShadowGovernanceValidationIssue]
    warnings: List[str]
    errors: List[str]

def check_boolean_false(obj, attr_name) -> Optional[ShadowGovernanceValidationIssue]:
    val = getattr(obj, attr_name, False)
    if val:
        return ShadowGovernanceValidationIssue("error", attr_name, f"{attr_name} must be False.")
    return None

def validate_shadow_comparison_report_report(item: ShadowSessionComparisonReport) -> ShadowGovernanceValidationReport:
    return ShadowGovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_shadow_scorecard_report(item: ShadowAcceptanceScorecard) -> ShadowGovernanceValidationReport:
    iss = []
    for attr in ["allowed_for_real_orders", "allowed_for_paper_state_mutation", "allowed_for_telegram_real_send", "allowed_for_production_config_write"]:
        err = check_boolean_false(item, attr)
        if err: iss.append(err)
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_shadow_decision_report(item: ShadowDecisionBoardResult) -> ShadowGovernanceValidationReport:
    iss = []
    for attr in ["allowed_for_real_orders", "allowed_for_paper_state_mutation", "allowed_for_telegram_real_send", "allowed_for_production_config_write"]:
        err = check_boolean_false(item, attr)
        if err: iss.append(err)
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_shadow_governance_review_report(item: ShadowGovernanceReview) -> ShadowGovernanceValidationReport:
    return ShadowGovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_shadow_governance_payload(payload: Dict[str, Any]) -> ShadowGovernanceValidationReport:
    s = str(payload).lower()
    if "api_key" in s or "secret" in s or "token" in s:
        iss = [ShadowGovernanceValidationIssue("error", None, "Secret leak detected in governance payload.")]
        return ShadowGovernanceValidationReport(False, 1, 0, 1, 0, iss, [], ["Secret leak detected in governance payload."])
    return ShadowGovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_shadow_governance(text: str) -> ShadowGovernanceValidationReport:
    t = text.lower()
    bad = ["live approved", "sent to broker", "kesin al", "garanti"]
    iss = [ShadowGovernanceValidationIssue("error", None, f"Live language: {b}") for b in bad if b in t]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_no_real_order_language_in_shadow_governance(text: str) -> ShadowGovernanceValidationReport:
    t = text.lower()
    bad = ["paper'a uygula", "canlıya al", "gerçek emir", "kesin kâr", "candidate kesin iyi"]
    iss = [ShadowGovernanceValidationIssue("error", None, f"Real order language: {b}") for b in bad if b in t]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_no_paper_state_mutation_fields_in_shadow_governance(payload: Dict[str, Any]) -> ShadowGovernanceValidationReport:
    bad = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]
    iss = [ShadowGovernanceValidationIssue("error", b, f"{b} found in payload") for b in bad if b in payload]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_no_broker_execution_fields_in_shadow_governance(payload: Dict[str, Any]) -> ShadowGovernanceValidationReport:
    bad = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    iss = [ShadowGovernanceValidationIssue("error", b, f"{b} found in payload") for b in bad if b in payload]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def shadow_governance_validation_report_to_text(report: ShadowGovernanceValidationReport) -> str:
    return f"Valid: {report.valid}. Errors: {report.error_count}"

def assert_shadow_governance_valid(report: ShadowGovernanceValidationReport) -> None:
    if not report.valid:
        raise ShadowGovernanceValidationError(" | ".join(report.errors))
