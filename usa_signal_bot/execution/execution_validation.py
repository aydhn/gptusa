from dataclasses import dataclass, field
from typing import Any
import json

from usa_signal_bot.core.exceptions import ExecutionValidationError
from usa_signal_bot.execution.liquidity_models import (
    LiquidityProfile,
    TradabilityGuardResult,
    BorrowabilityProxyResult,
    ExecutionRealismReview
)

@dataclass
class ExecutionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ExecutionValidationIssue]
    warnings: list[str]
    errors: list[str]


def validate_liquidity_profile_report(profile: LiquidityProfile) -> ExecutionValidationReport:
    issues = []
    errors = []

    if profile.avg_daily_volume is not None and profile.avg_daily_volume < 0:
        errors.append("Negative volume found")
        issues.append(ExecutionValidationIssue("ERROR", "avg_daily_volume", "Negative volume"))

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_tradability_guard_report(result: TradabilityGuardResult) -> ExecutionValidationReport:
    issues = []
    errors = []

    if result.slippage_estimate and result.slippage_estimate.slippage_proxy_bps is not None and result.slippage_estimate.slippage_proxy_bps < 0:
        errors.append("Negative slippage found")
        issues.append(ExecutionValidationIssue("ERROR", "slippage_proxy_bps", "Negative slippage"))

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_borrowability_proxy_report(result: BorrowabilityProxyResult) -> ExecutionValidationReport:
    issues = []
    errors = []

    if result.score is not None and (result.score < 0 or result.score > 100):
        errors.append("Score out of range")
        issues.append(ExecutionValidationIssue("ERROR", "score", "Score out of range"))

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_execution_realism_review_report(review: ExecutionRealismReview) -> ExecutionValidationReport:
    issues = []
    errors = []

    for p in review.liquidity_profiles:
        r = validate_liquidity_profile_report(p)
        issues.extend(r.issues)
        errors.extend(r.errors)

    for t in review.tradability_results:
        r = validate_tradability_guard_report(t)
        issues.extend(r.issues)
        errors.extend(r.errors)

    for b in review.borrowability_results:
        r = validate_borrowability_proxy_report(b)
        issues.extend(r.issues)
        errors.extend(r.errors)

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_sensitive_data_in_execution_payload(payload: dict[str, Any]) -> ExecutionValidationReport:
    issues = []
    errors = []

    payload_str = json.dumps(payload).lower()

    sensitive_keys = ["api_key", "secret", "token", "password", "credential"]
    for k in sensitive_keys:
        if k in payload_str:
            errors.append(f"Sensitive key {k} leaked in payload")
            issues.append(ExecutionValidationIssue("ERROR", None, f"Sensitive data leak: {k}"))

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_live_execution_language_in_execution(text: str) -> ExecutionValidationReport:
    issues = []
    errors = []

    text_lower = text.lower()

    forbidden_terms = [
        "live approved", "sent to broker", "kesin al", "garanti",
        "order sent", "live execution", "live order", "broker accepted",
        "definitely shortable", "borrow guaranteed"
    ]

    for t in forbidden_terms:
        if t in text_lower:
            errors.append(f"Forbidden language found: {t}")
            issues.append(ExecutionValidationIssue("ERROR", None, f"Forbidden language found: {t}"))

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_broker_execution_fields(payload: dict[str, Any]) -> ExecutionValidationReport:
    issues = []
    errors = []

    payload_str = json.dumps(payload).lower()

    forbidden_keys = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue"]

    for k in forbidden_keys:
        if k in payload_str:
            errors.append(f"Forbidden broker field found: {k}")
            issues.append(ExecutionValidationIssue("ERROR", None, f"Forbidden broker field found: {k}"))

    return ExecutionValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def execution_validation_report_to_text(report: ExecutionValidationReport) -> str:
    lines = [
        "Execution Validation Report",
        f"  Valid: {report.valid}",
        f"  Errors: {report.error_count}"
    ]
    for i in report.issues:
        lines.append(f"   - {i.severity}: {i.message} ({i.field})")
    return "\n".join(lines)

def assert_execution_valid(report: ExecutionValidationReport) -> None:
    if not report.valid:
        raise ExecutionValidationError("Execution validation failed: " + str(report.errors))
