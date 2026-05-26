from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeContext,
    ProviderFreezeFullReview
)
from usa_signal_bot.provider_freeze.freeze_safety_validator import freeze_text_has_trade_or_execution_language
from usa_signal_bot.core.exceptions import ProviderFreezeValidationError

@dataclass
class ProviderFreezeValidationIssue:
    severity: str
    field: Optional[str] = None
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFreezeValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[ProviderFreezeValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _add_issue(report: ProviderFreezeValidationReport, sev: str, msg: str, fld: Optional[str] = None):
    report.issues.append(ProviderFreezeValidationIssue(severity=sev, message=msg, field=fld))
    report.issue_count += 1
    if sev == "WARNING":
        report.warning_count += 1
        report.warnings.append(msg)
    elif sev == "ERROR":
        report.error_count += 1
        report.errors.append(msg)
    elif sev == "BLOCK":
        report.blocked_count += 1
        report.errors.append(msg)

def validate_provider_freeze_context_report(item: ProviderFreezeContext) -> ProviderFreezeValidationReport:
    r = ProviderFreezeValidationReport()

    if item.activation_allowed: _add_issue(r, "BLOCK", "activation_allowed is True")
    if item.active_paper_enabled: _add_issue(r, "BLOCK", "active_paper_enabled is True")
    if item.broker_execution_enabled: _add_issue(r, "BLOCK", "broker_execution_enabled is True")
    if item.order_creation_enabled: _add_issue(r, "BLOCK", "order_creation_enabled is True")
    if item.paper_state_mutation_enabled: _add_issue(r, "BLOCK", "paper_state_mutation_enabled is True")
    if item.telegram_real_send_enabled: _add_issue(r, "BLOCK", "telegram_real_send_enabled is True")
    if item.scraping_enabled: _add_issue(r, "BLOCK", "scraping_enabled is True")
    if item.html_parse_enabled: _add_issue(r, "BLOCK", "html_parse_enabled is True")
    if item.paid_api_enabled: _add_issue(r, "BLOCK", "paid_api_enabled is True")
    if item.dashboard_enabled: _add_issue(r, "BLOCK", "dashboard_enabled is True")
    if item.network_default_enabled: _add_issue(r, "BLOCK", "network_default_enabled is True")

    if item.network_used: _add_issue(r, "BLOCK", "network_used is True")
    if item.paid_api_used: _add_issue(r, "BLOCK", "paid_api_used is True")
    if item.scraping_used: _add_issue(r, "BLOCK", "scraping_used is True")
    if item.html_parsing_used: _add_issue(r, "BLOCK", "html_parsing_used is True")
    if item.broker_used: _add_issue(r, "BLOCK", "broker_used is True")
    if item.order_created: _add_issue(r, "BLOCK", "order_created is True")
    if item.paper_state_mutated: _add_issue(r, "BLOCK", "paper_state_mutated is True")
    if item.telegram_real_sent: _add_issue(r, "BLOCK", "telegram_real_sent is True")
    if item.dashboard_started: _add_issue(r, "BLOCK", "dashboard_started is True")

    if item.produces_trade_signal: _add_issue(r, "BLOCK", "produces_trade_signal is True")
    if item.produces_order_decision: _add_issue(r, "BLOCK", "produces_order_decision is True")

    r.valid = (r.error_count == 0 and r.blocked_count == 0)
    return r

def validate_provider_freeze_full_review_report(item: ProviderFreezeFullReview) -> ProviderFreezeValidationReport:
    r = validate_provider_freeze_context_report(item.context)
    if not item.freeze_bundle.freeze_valid:
        _add_issue(r, "ERROR", "Freeze bundle is invalid.")
    if not item.multi_provider_review.multi_provider_review_passed:
        _add_issue(r, "ERROR", "Multi-provider review failed.")
    if not item.rehearsal_report.rehearsal_passed:
        _add_issue(r, "ERROR", "Data layer rehearsal failed.")
    r.valid = (r.error_count == 0 and r.blocked_count == 0)
    return r

def validate_no_sensitive_data_in_freeze_payload(payload: Dict[str, Any]) -> ProviderFreezeValidationReport:
    r = ProviderFreezeValidationReport(valid=True)
    # Simple check for keys containing 'secret', 'password', 'token', 'key'
    def check_dict(d: dict):
        for k, v in d.items():
            lk = k.lower()
            if any(s in lk for s in ["secret", "password", "token", "api_key", "apikey"]):
                _add_issue(r, "BLOCK", f"Sensitive key found: {k}")
            if isinstance(v, dict):
                check_dict(v)
            elif isinstance(v, list):
                for i in v:
                    if isinstance(i, dict):
                        check_dict(i)
    check_dict(payload)
    r.valid = (r.error_count == 0 and r.blocked_count == 0)
    return r

def validate_no_execution_language_in_freeze_text(text: str) -> ProviderFreezeValidationReport:
    r = ProviderFreezeValidationReport(valid=True)
    if freeze_text_has_trade_or_execution_language(text):
        _add_issue(r, "BLOCK", "Text contains execution or trade signal language.")
        r.valid = False
    return r

def validate_no_unsafe_freeze_fields(payload: Dict[str, Any]) -> ProviderFreezeValidationReport:
    r = ProviderFreezeValidationReport(valid=True)
    unsafe = [
        "broker_order_id", "live_order_id", "sent_to_broker",
        "activation_allowed", "active_paper_enabled", "broker_execution_enabled"
    ]
    def check_dict(d: dict):
        for k, v in d.items():
            if k in unsafe:
                if v: # if true or truthy
                    _add_issue(r, "BLOCK", f"Unsafe field is true/present: {k}")
            if isinstance(v, dict):
                check_dict(v)
    check_dict(payload)
    r.valid = (r.error_count == 0 and r.blocked_count == 0)
    return r

def provider_freeze_validation_report_to_text(report: ProviderFreezeValidationReport) -> str:
    lines = [f"Provider Freeze Validation Report: Valid={report.valid}"]
    for i in report.issues:
        lines.append(f" - [{i.severity}] {i.field or ''}: {i.message}")
    return "\n".join(lines)

def assert_provider_freeze_validation_valid(report: ProviderFreezeValidationReport) -> None:
    if not report.valid:
        raise ProviderFreezeValidationError("Provider Freeze validation failed:\n" + provider_freeze_validation_report_to_text(report))
