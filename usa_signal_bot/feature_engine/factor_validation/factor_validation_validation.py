from typing import Any
from dataclasses import dataclass
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorValidationContext,
    FactorValidationFullReview
)
from usa_signal_bot.core.exceptions import FactorValidationValidationError

@dataclass
class FactorValidationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class FactorValidationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[FactorValidationValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_factor_validation_context_report(item: FactorValidationContext) -> FactorValidationValidationReport:
    return validate_no_unsafe_factor_validation_fields(item.__dict__)

def validate_factor_validation_full_review_report(item: FactorValidationFullReview) -> FactorValidationValidationReport:
    return validate_no_unsafe_factor_validation_fields(item.__dict__)

def validate_no_sensitive_data_in_factor_validation_payload(payload: dict[str, Any]) -> FactorValidationValidationReport:
    # simple mock
    return validate_no_unsafe_factor_validation_fields(payload)

def validate_no_execution_language_in_factor_validation_text(text: str) -> FactorValidationValidationReport:
    issues = []
    if any(x in text.lower() for x in ['buy_signal', 'sell_signal', 'portfolio_weight', 'target_weight', 'allocation', 'emir gönderildi']):
        issues.append(FactorValidationValidationIssue("ERROR", None, "Execution language found", {}))

    return FactorValidationValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_unsafe_factor_validation_fields(payload: dict[str, Any]) -> FactorValidationValidationReport:
    issues = []
    unsafe_keys = [
        "activation_allowed", "strategy_activation_allowed", "active_paper_enabled",
        "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled",
        "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "network_used", "paid_api_used", "scraping_used", "html_parsing_used",
        "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent",
        "dashboard_started", "produces_trade_signal", "produces_order_decision",
        "produces_portfolio_weights", "produced_trade_signal", "produced_order_decision",
        "produced_portfolio_weights"
    ]

    def check_dict(d):
        if not isinstance(d, dict): return
        for k, v in d.items():
            if k in unsafe_keys and v is True:
                issues.append(FactorValidationValidationIssue("ERROR", k, f"{k} is True", {}))
            elif isinstance(v, dict):
                check_dict(v)
            elif isinstance(v, list):
                for i in v:
                    check_dict(i)

    check_dict(payload)

    return FactorValidationValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def factor_validation_validation_report_to_text(report: FactorValidationValidationReport) -> str:
    return f"Report valid: {report.valid}, Errors: {report.error_count}"

def assert_factor_validation_validation_valid(report: FactorValidationValidationReport) -> None:
    if not report.valid:
        raise FactorValidationValidationError(f"Validation failed: {report.errors}")
