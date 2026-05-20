from dataclasses import dataclass, field
from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowPortfolioState, ShadowRehearsalSession, ShadowRehearsalReview
)
from usa_signal_bot.paper_shadow.shadow_validator import validate_shadow_session_safety

@dataclass
class ShadowValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ShadowValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_shadow_context_report(item: ShadowSimulationContext) -> ShadowValidationReport:
    errors = []
    if item.allow_real_orders or item.allow_broker_calls or item.allow_paper_state_mutation or item.allow_telegram_real_send or item.allow_production_config_write:
        errors.append("Unsafe allow flags set in context.")

    issues = [ShadowValidationIssue(severity="ERROR", field="allow_flags", message=e) for e in errors]
    return ShadowValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_shadow_portfolio_report(item: ShadowPortfolioState) -> ShadowValidationReport:
    return ShadowValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_shadow_session_report(item: ShadowRehearsalSession) -> ShadowValidationReport:
    errors = validate_shadow_session_safety(item)
    issues = [ShadowValidationIssue(severity="ERROR", field="safety", message=e) for e in errors]
    return ShadowValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_shadow_review_report(item: ShadowRehearsalReview) -> ShadowValidationReport:
    return ShadowValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_shadow_payload(payload: Dict[str, Any]) -> ShadowValidationReport:
    return ShadowValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_shadow(text: str) -> ShadowValidationReport:
    errors = []
    text_lower = text.lower()
    for forbidden in ["live approved", "sent to broker", "kesin al", "garanti", "canlıya al", "gerçek emir"]:
        if forbidden in text_lower:
            errors.append(f"Forbidden phrase found: {forbidden}")
    return ShadowValidationReport(len(errors) == 0, len(errors), 0, len(errors), 0, [], [], errors)

def validate_no_real_order_language_in_shadow(text: str) -> ShadowValidationReport:
    return validate_no_live_execution_language_in_shadow(text)

def validate_no_paper_state_mutation_fields_in_shadow(payload: Dict[str, Any]) -> ShadowValidationReport:
    errors = []
    for field in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if payload.get(field):
            errors.append(f"Forbidden field found: {field}")
    return ShadowValidationReport(len(errors) == 0, len(errors), 0, len(errors), 0, [], [], errors)

def validate_no_broker_execution_fields_in_shadow(payload: Dict[str, Any]) -> ShadowValidationReport:
    errors = []
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if payload.get(field):
            errors.append(f"Forbidden broker field found: {field}")
    return ShadowValidationReport(len(errors) == 0, len(errors), 0, len(errors), 0, [], [], errors)

def shadow_validation_report_to_text(report: ShadowValidationReport) -> str:
    return f"ShadowValidationReport(valid={report.valid}, errors={report.error_count})"

def assert_shadow_valid(report: ShadowValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Shadow validation failed: {report.errors}")
