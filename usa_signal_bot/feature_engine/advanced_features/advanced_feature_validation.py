from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from usa_signal_bot.feature_engine.advanced_features.phase118_models import AdvancedFeatureContext, AdvancedFeatureFullReview
from usa_signal_bot.core.exceptions import AdvancedFeatureValidationError
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_output_safety_validator import advanced_feature_output_text_has_trade_or_execution_language

@dataclass
class AdvancedFeatureValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any]

@dataclass
class AdvancedFeatureValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AdvancedFeatureValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_no_unsafe_advanced_feature_fields(payload: Dict[str, Any]) -> AdvancedFeatureValidationReport:
    errors = []

    # Simple recursive payload check
    def check_dict(d):
        for k, v in d.items():
            if isinstance(v, dict):
                check_dict(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        check_dict(item)
            elif isinstance(v, bool) and v is True:
                if k in ["activation_allowed", "active_paper_enabled", "broker_execution_enabled",
                         "order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
                         "scraping_enabled", "html_parse_enabled", "paid_api_enabled", "dashboard_enabled",
                         "network_default_enabled", "network_used", "paid_api_used", "scraping_used",
                         "html_parsing_used", "broker_used", "order_created", "paper_state_mutated",
                         "telegram_real_sent", "dashboard_started", "produces_trade_signal",
                         "produces_order_decision", "produces_portfolio_weights", "produced_trade_signal",
                         "produced_order_decision", "produced_portfolio_weights"]:
                    errors.append(f"Forbidden true value on field {k}")

    check_dict(payload)

    issues = [AdvancedFeatureValidationIssue(severity="ERROR", field=None, message=e, details={}) for e in errors]
    return AdvancedFeatureValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_sensitive_data_in_advanced_feature_payload(payload: Dict[str, Any]) -> AdvancedFeatureValidationReport:
    # Just basic check
    import json
    text = json.dumps(payload).lower()
    errors = []
    if "api_key" in text or "token" in text or "secret" in text or "password" in text:
        errors.append("Potential leak of secret/token/password")
    if "broker_order_id" in text or "live_order_id" in text or "sent_to_broker" in text:
        errors.append("Broker execution id found in payload")

    issues = [AdvancedFeatureValidationIssue(severity="ERROR", field=None, message=e, details={}) for e in errors]
    return AdvancedFeatureValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_execution_language_in_advanced_feature_text(text: str) -> AdvancedFeatureValidationReport:
    errors = []
    if advanced_feature_output_text_has_trade_or_execution_language(text):
        errors.append("Execution language detected in text.")

    issues = [AdvancedFeatureValidationIssue(severity="ERROR", field=None, message=e, details={}) for e in errors]
    return AdvancedFeatureValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_advanced_feature_context_report(item: AdvancedFeatureContext) -> AdvancedFeatureValidationReport:
    from usa_signal_bot.feature_engine.advanced_features.phase118_models import advanced_feature_context_to_dict
    payload = advanced_feature_context_to_dict(item)
    return validate_no_unsafe_advanced_feature_fields(payload)

def validate_advanced_feature_full_review_report(item: AdvancedFeatureFullReview) -> AdvancedFeatureValidationReport:
    from usa_signal_bot.feature_engine.advanced_features.phase118_models import advanced_feature_full_review_to_dict
    payload = advanced_feature_full_review_to_dict(item)
    return validate_no_unsafe_advanced_feature_fields(payload)

def advanced_feature_validation_report_to_text(report: AdvancedFeatureValidationReport) -> str:
    if report.valid:
        return "Validation Report: PASSED."
    return f"Validation Report: FAILED. {report.error_count} errors.\n" + "\n".join(report.errors)

def assert_advanced_feature_validation_valid(report: AdvancedFeatureValidationReport) -> None:
    if not report.valid:
        raise AdvancedFeatureValidationError(advanced_feature_validation_report_to_text(report))
