from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelingContext,
    RegimeLabelingFullReview
)
from usa_signal_bot.core.exceptions import RegimeLabelingValidationError

@dataclass
class RegimeLabelingValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeLabelingValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[RegimeLabelingValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_no_unsafe_regime_labeling_fields(payload: dict[str, Any]) -> RegimeLabelingValidationReport:
    issues = []
    unsafe_fields = [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
        "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
        "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "network_used", "paid_api_used", "scraping_used", "html_parsing_used", "broker_used",
        "order_created", "paper_state_mutated", "telegram_real_sent", "dashboard_started",
        "model_training_used", "model_prediction_used", "heavy_ml_dependency_used",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
        "investment_advice"
    ]

    for f in unsafe_fields:
        if payload.get(f, False) is True:
            issues.append(RegimeLabelingValidationIssue("ERROR", f, f"{f} must be false", {}))

    return RegimeLabelingValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues]
    )

def validate_no_sensitive_data_in_regime_labeling_payload(payload: dict[str, Any]) -> RegimeLabelingValidationReport:
    issues = []
    sensitive = ["api_key", "token", "secret", "password", "broker_order_id", "live_order_id", "sent_to_broker"]

    # simplistic dict check
    payload_str = str(payload).lower()
    for s in sensitive:
        if s in payload_str:
            issues.append(RegimeLabelingValidationIssue("ERROR", None, f"Sensitive data found: {s}", {}))

    return RegimeLabelingValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues]
    )

def validate_no_execution_language_in_regime_labeling_text(text: str) -> RegimeLabelingValidationReport:
    issues = []
    forbidden = [
        "buy_signal", "sell_signal", "portfolio_weight", "target_weight", "allocation",
        "deploy", "production_patch", "emir gönderildi", "aktif trading başladı",
        "paper'a alındı", "canlıya alındı", "kesin al", "kesin sat", "güçlü al",
        "güçlü sat", "garanti kâr", "buy signal", "sell signal", "strong buy", "strong sell"
    ]

    text_lower = text.lower()
    for f in forbidden:
        if f in text_lower:
            issues.append(RegimeLabelingValidationIssue("ERROR", None, f"Execution language found: {f}", {}))

    return RegimeLabelingValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues]
    )

def validate_regime_labeling_context_report(item: RegimeLabelingContext) -> RegimeLabelingValidationReport:
    from usa_signal_bot.regime_classification.labeling.phase128_models import regime_labeling_context_to_dict
    d = regime_labeling_context_to_dict(item)
    r1 = validate_no_unsafe_regime_labeling_fields(d)
    r2 = validate_no_sensitive_data_in_regime_labeling_payload(d)

    issues = r1.issues + r2.issues

    if item.model_training_used or item.model_prediction_used:
        issues.append(RegimeLabelingValidationIssue("ERROR", "model", "Model training/prediction used", {}))

    return RegimeLabelingValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        errors=[i.message for i in issues]
    )

def validate_regime_labeling_full_review_report(item: RegimeLabelingFullReview) -> RegimeLabelingValidationReport:
    return validate_regime_labeling_context_report(item.context)

def regime_labeling_validation_report_to_text(report: RegimeLabelingValidationReport) -> str:
    if report.valid:
        return "Validation passed."
    return f"Validation failed with {report.error_count} errors: {', '.join(report.errors[:3])}"

def assert_regime_labeling_validation_valid(report: RegimeLabelingValidationReport) -> None:
    if not report.valid:
        raise RegimeLabelingValidationError(regime_labeling_validation_report_to_text(report))
