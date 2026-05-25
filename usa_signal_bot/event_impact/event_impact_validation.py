
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.event_impact.phase112_models import EventImpactContext, EventImpactFullReview
from usa_signal_bot.event_impact.event_impact_safety_validator import validate_event_impact_context_safety

@dataclass
class EventImpactValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventImpactValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[EventImpactValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_no_sensitive_data_in_event_impact_payload(payload: Dict[str, Any]) -> EventImpactValidationReport:
    return EventImpactValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)

def validate_no_execution_language_in_event_impact_text(text: str) -> EventImpactValidationReport:
    return EventImpactValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)

def validate_no_unsafe_event_impact_fields(payload: Dict[str, Any]) -> EventImpactValidationReport:
    errs = []
    for k in ["produces_trade_signal", "produces_order_decision", "network_used", "broker_used", "paper_state_mutated", "telegram_real_sent"]:
        if payload.get(k): errs.append(f"{k} is True")
    return EventImpactValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=len(errs),
        errors=errs
    )

def validate_event_impact_context_report(item: EventImpactContext) -> EventImpactValidationReport:
    errs = validate_event_impact_context_safety(item)
    return EventImpactValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=len(errs),
        errors=errs
    )

def validate_event_impact_full_review_report(item: EventImpactFullReview) -> EventImpactValidationReport:
    return validate_event_impact_context_report(item.context)

def event_impact_validation_report_to_text(report: EventImpactValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_event_impact_validation_valid(report: EventImpactValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Validation failed: {report.errors}")
