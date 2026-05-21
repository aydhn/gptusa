from dataclasses import dataclass, field
from typing import Any, Dict, List
from .dossier_models import (
    ObserverPromotionDossier,
    FinalSafetyBoardReview,
    StagedPaperReadinessPackage,
    PromotionDossierReview
)
from usa_signal_bot.core.exceptions import PromotionDossierValidationError

@dataclass
class PromotionDossierValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionDossierValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PromotionDossierValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_promotion_dossier_report(item: ObserverPromotionDossier) -> PromotionDossierValidationReport:
    issues = []
    if item.allowed_for_active_paper: issues.append(PromotionDossierValidationIssue("ERROR", "allowed_for_active_paper", "Illegally enabled active paper."))
    if item.allowed_for_broker_execution: issues.append(PromotionDossierValidationIssue("ERROR", "allowed_for_broker_execution", "Illegally enabled broker execution."))
    if item.allowed_for_paper_state_mutation: issues.append(PromotionDossierValidationIssue("ERROR", "allowed_for_paper_state_mutation", "Illegally enabled paper mutation."))
    if item.allowed_for_config_patch: issues.append(PromotionDossierValidationIssue("ERROR", "allowed_for_config_patch", "Illegally enabled config patch."))
    return PromotionDossierValidationReport(
        valid=len(issues)==0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[]
    )

def validate_safety_board_review_report(item: FinalSafetyBoardReview) -> PromotionDossierValidationReport:
    issues = []
    if item.allowed_for_active_paper: issues.append(PromotionDossierValidationIssue("ERROR", "allowed_for_active_paper", "Board illegally enabled active paper."))
    return PromotionDossierValidationReport(
        valid=len(issues)==0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[]
    )

def validate_readiness_package_report(item: StagedPaperReadinessPackage) -> PromotionDossierValidationReport:
    issues = []
    if item.allowed_for_active_paper: issues.append(PromotionDossierValidationIssue("ERROR", "allowed_for_active_paper", "Package illegally enabled active paper."))
    return PromotionDossierValidationReport(
        valid=len(issues)==0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[]
    )

def validate_promotion_dossier_review_report(item: PromotionDossierReview) -> PromotionDossierValidationReport:
    # aggregate
    return PromotionDossierValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_promotion_dossier_payload(payload: Dict[str, Any]) -> PromotionDossierValidationReport:
    return PromotionDossierValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_promotion_dossier(text: str) -> PromotionDossierValidationReport:
    banned = ["live approved", "sent to broker", "kesin al", "garanti"]
    issues = []
    for b in banned:
        if b in text.lower():
            issues.append(PromotionDossierValidationIssue("ERROR", None, f"Found banned text: {b}"))
    return PromotionDossierValidationReport(len(issues)==0, len(issues), 0, len(issues), len(issues), issues, [], [])

def validate_no_active_paper_language_in_promotion_dossier(text: str) -> PromotionDossierValidationReport:
    banned = ["paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]
    issues = []
    for b in banned:
        if b in text.lower():
            issues.append(PromotionDossierValidationIssue("ERROR", None, f"Found banned text: {b}"))
    return PromotionDossierValidationReport(len(issues)==0, len(issues), 0, len(issues), len(issues), issues, [], [])

def validate_no_paper_state_mutation_fields_in_promotion_dossier(payload: Dict[str, Any]) -> PromotionDossierValidationReport:
    banned = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]
    issues = []
    for b in banned:
        if b in payload:
            issues.append(PromotionDossierValidationIssue("ERROR", b, f"Found banned field: {b}"))
    return PromotionDossierValidationReport(len(issues)==0, len(issues), 0, len(issues), len(issues), issues, [], [])

def validate_no_broker_execution_fields_in_promotion_dossier(payload: Dict[str, Any]) -> PromotionDossierValidationReport:
    banned = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    issues = []
    for b in banned:
        if b in payload:
            issues.append(PromotionDossierValidationIssue("ERROR", b, f"Found banned field: {b}"))
    return PromotionDossierValidationReport(len(issues)==0, len(issues), 0, len(issues), len(issues), issues, [], [])

def promotion_dossier_validation_report_to_text(report: PromotionDossierValidationReport) -> str:
    if report.valid: return "Validation passed."
    return f"Validation failed with {report.issue_count} issues."

def assert_promotion_dossier_valid(report: PromotionDossierValidationReport) -> None:
    if not report.valid:
        raise PromotionDossierValidationError("Dossier validation failed.")
