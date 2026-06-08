from dataclasses import dataclass, field
from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionContext,
    PortfolioConstructionFullReview
)
from usa_signal_bot.core.exceptions import PortfolioConstructionValidationError

@dataclass
class PortfolioConstructionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any]

@dataclass
class PortfolioConstructionValidationReportEnvelope:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PortfolioConstructionValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_portfolio_construction_context_report(item: PortfolioConstructionContext) -> PortfolioConstructionValidationReportEnvelope:
    from usa_signal_bot.portfolio.construction.portfolio_construction_safety_validator import validate_portfolio_construction_context_safety
    from usa_signal_bot.portfolio.construction.portfolio_construction_schema_validator import validate_portfolio_construction_context_schema

    schema_errs = validate_portfolio_construction_context_schema(item)
    safety_errs = validate_portfolio_construction_context_safety(item)

    all_errs = schema_errs + safety_errs
    issues = [
        PortfolioConstructionValidationIssue("ERROR", None, err, {}) for err in all_errs
    ]

    return PortfolioConstructionValidationReportEnvelope(
        valid=len(all_errs) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(all_errs),
        blocked_count=1 if not item.ready_for_phase156 else 0,
        issues=issues,
        warnings=[],
        errors=all_errs
    )

def validate_portfolio_construction_full_review_report(item: PortfolioConstructionFullReview) -> PortfolioConstructionValidationReportEnvelope:
    return validate_portfolio_construction_context_report(item.context)

def validate_no_sensitive_data_in_portfolio_construction_payload(payload: Dict[str, Any]) -> PortfolioConstructionValidationReportEnvelope:
    issues = []
    # simplistic secret check
    def _search(obj: Any):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if "api_key" in k.lower() or "secret" in k.lower() or "token" in k.lower():
                    issues.append(PortfolioConstructionValidationIssue("ERROR", k, f"Potential sensitive field: {k}", {}))
                _search(v)
        elif isinstance(obj, list):
            for item in obj:
                _search(item)
    _search(payload)

    return PortfolioConstructionValidationReportEnvelope(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_execution_language_in_portfolio_construction_text(text: str) -> PortfolioConstructionValidationReportEnvelope:
    from usa_signal_bot.portfolio.construction.portfolio_construction_safety_validator import portfolio_construction_text_has_trade_or_execution_language

    has_exec = portfolio_construction_text_has_trade_or_execution_language(text)
    issues = []
    if has_exec:
        issues.append(PortfolioConstructionValidationIssue("ERROR", None, "Execution language detected in text.", {}))

    return PortfolioConstructionValidationReportEnvelope(
        valid=not has_exec,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_unsafe_portfolio_construction_fields(payload: Dict[str, Any]) -> PortfolioConstructionValidationReportEnvelope:
    from usa_signal_bot.portfolio.construction.portfolio_construction_input_resolver import detect_forbidden_construction_fields

    fields = detect_forbidden_construction_fields(payload)
    issues = []
    for f in fields:
        issues.append(PortfolioConstructionValidationIssue("ERROR", f, f"Forbidden field: {f}", {}))

    return PortfolioConstructionValidationReportEnvelope(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def portfolio_construction_validation_report_to_text(report: PortfolioConstructionValidationReportEnvelope) -> str:
    if report.valid:
        return "Validation OK."
    return f"Validation Failed: {report.error_count} errors.\n" + "\n".join(f"- {e}" for e in report.errors)

def assert_portfolio_construction_validation_valid(report: PortfolioConstructionValidationReportEnvelope) -> None:
    if not report.valid:
        raise PortfolioConstructionValidationError(f"Validation failed: {report.errors[0]}" if report.errors else "Validation failed.")
