from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardContext,
    WalkForwardFullReview
)
from usa_signal_bot.backtesting.walk_forward.walk_forward_safety_validator import walk_forward_text_has_trade_or_execution_language
from usa_signal_bot.core.exceptions import WalkForwardValidationError

@dataclass
class WalkForwardValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WalkForwardValidationReportEnvelope:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[WalkForwardValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_walk_forward_context_report(item: WalkForwardContext) -> WalkForwardValidationReportEnvelope:
    env = WalkForwardValidationReportEnvelope(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    if not item.phase151_readiness_gate.ready_for_phase151:
        env.valid = False
        env.errors.append("Context is not ready for Phase 151")
        env.error_count += 1
    return env

def validate_walk_forward_full_review_report(item: WalkForwardFullReview) -> WalkForwardValidationReportEnvelope:
    return validate_walk_forward_context_report(item.context)

def validate_no_sensitive_data_in_walk_forward_payload(payload: Dict[str, Any]) -> WalkForwardValidationReportEnvelope:
    env = WalkForwardValidationReportEnvelope(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    # Mock
    return env

def validate_no_execution_language_in_walk_forward_text(text: str) -> WalkForwardValidationReportEnvelope:
    env = WalkForwardValidationReportEnvelope(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    if walk_forward_text_has_trade_or_execution_language(text):
        env.valid = False
        env.errors.append("Execution language found")
        env.error_count += 1
    return env

def validate_no_unsafe_walk_forward_fields(payload: Dict[str, Any]) -> WalkForwardValidationReportEnvelope:
    env = WalkForwardValidationReportEnvelope(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    # Mock
    return env

def walk_forward_validation_report_to_text(report: WalkForwardValidationReportEnvelope) -> str:
    return "Valid" if report.valid else f"Invalid ({report.error_count} errors)"

def assert_walk_forward_validation_valid(report: WalkForwardValidationReportEnvelope) -> None:
    if not report.valid:
        raise WalkForwardValidationError(f"Walk Forward Validation failed: {report.errors}")
