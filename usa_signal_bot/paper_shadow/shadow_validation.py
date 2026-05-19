import dataclasses
from dataclasses import dataclass
from typing import Any
from dataclasses import field
import json
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowPortfolioState,
    ShadowRehearsalSession,
    ShadowRehearsalReview
)
from usa_signal_bot.core.exceptions import ShadowValidationError

@dataclass
class ShadowValidationIssue:
    severity: str
    message: str
    field: str | None = None
    details: dict = dataclasses.field(default_factory=dict)

@dataclass
class ShadowValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ShadowValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_shadow_context_report(item: ShadowSimulationContext) -> ShadowValidationReport:
    issues = []
    if item.allow_real_orders: issues.append(ShadowValidationIssue("ERROR", "allow_real_orders is True", "allow_real_orders"))
    if item.allow_broker_calls: issues.append(ShadowValidationIssue("ERROR", "allow_broker_calls is True", "allow_broker_calls"))
    if item.allow_paper_state_mutation: issues.append(ShadowValidationIssue("ERROR", "allow_paper_state_mutation is True", "allow_paper_state_mutation"))
    if item.allow_telegram_real_send: issues.append(ShadowValidationIssue("ERROR", "allow_telegram_real_send is True", "allow_telegram_real_send"))
    if item.allow_production_config_write: issues.append(ShadowValidationIssue("ERROR", "allow_production_config_write is True", "allow_production_config_write"))
    return _build_report(issues)

def validate_shadow_portfolio_report(item: ShadowPortfolioState) -> ShadowValidationReport:
    return _build_report([]) # Simplified for mock

def validate_shadow_session_report(item: ShadowRehearsalSession) -> ShadowValidationReport:
    issues = []
    if item.context:
        rep = validate_shadow_context_report(item.context)
        issues.extend(rep.issues)
    for intent in item.order_intents:
        if intent.is_real_order:
             issues.append(ShadowValidationIssue("ERROR", "is_real_order is True", "is_real_order"))
        if intent.broker_destination:
             issues.append(ShadowValidationIssue("ERROR", "broker_destination is not None", "broker_destination"))
    for fill in item.fills:
        if fill.is_real_fill:
             issues.append(ShadowValidationIssue("ERROR", "is_real_fill is True", "is_real_fill"))
    return _build_report(issues)

def validate_shadow_review_report(item: ShadowRehearsalReview) -> ShadowValidationReport:
    issues = []
    for session in item.sessions:
        rep = validate_shadow_session_report(session)
        issues.extend(rep.issues)
    return _build_report(issues)

def validate_no_sensitive_data_in_shadow_payload(payload: dict[str, Any]) -> ShadowValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    for term in ["secret", "token", "password", "api_key"]:
        if term in payload_str:
            issues.append(ShadowValidationIssue("ERROR", f"Potential sensitive data: {term}"))
    return _build_report(issues)

def validate_no_live_execution_language_in_shadow(text: str) -> ShadowValidationReport:
    issues = []
    text_lower = text.lower()
    for term in ["live approved", "sent to broker", "kesin al", "garanti"]:
        if term in text_lower:
             issues.append(ShadowValidationIssue("ERROR", f"Live execution language detected: {term}"))
    return _build_report(issues)

def validate_no_real_order_language_in_shadow(text: str) -> ShadowValidationReport:
    issues = []
    text_lower = text.lower()
    for term in ["paper'a uygula", "canlıya al", "gerçek emir", "kesin kâr", "candidate kesin iyi"]:
        if term in text_lower:
             issues.append(ShadowValidationIssue("ERROR", f"Real order language detected: {term}"))
    return _build_report(issues)

def validate_no_paper_state_mutation_fields_in_shadow(payload: dict[str, Any]) -> ShadowValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    for term in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if f'"{term}": true' in payload_str:
             issues.append(ShadowValidationIssue("ERROR", f"Paper state mutation field detected: {term}"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_shadow(payload: dict[str, Any]) -> ShadowValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    for term in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f'"{term}"' in payload_str:
             issues.append(ShadowValidationIssue("ERROR", f"Broker execution field detected: {term}"))
    return _build_report(issues)

def shadow_validation_report_to_text(report: ShadowValidationReport) -> str:
    text = "Shadow Validation Report\n"
    text += f"Valid: {report.valid}\n"
    text += f"Issues: {report.issue_count} (Errors: {report.error_count}, Warnings: {report.warning_count}, Blocked: {report.blocked_count})\n"
    for issue in report.issues:
        text += f"- [{issue.severity}] {issue.message}\n"
    return text

def assert_shadow_valid(report: ShadowValidationReport) -> None:
    if not report.valid:
        raise ShadowValidationError(f"Shadow validation failed: {report.error_count} errors.")

def _build_report(issues: list[ShadowValidationIssue]) -> ShadowValidationReport:
    return ShadowValidationReport(
        valid=not any(i.severity in ["ERROR", "BLOCK"] for i in issues),
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "WARNING"),
        error_count=sum(1 for i in issues if i.severity == "ERROR"),
        blocked_count=sum(1 for i in issues if i.severity == "BLOCK"),
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity in ["ERROR", "BLOCK"]]
    )
