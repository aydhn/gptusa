import json
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    SymbolRegimeAlignment,
    RegimeTransitionSignal,
    RegimeMapReview,
    validate_timeframe_regime_snapshot,
    validate_multi_timeframe_regime_confirmation,
    validate_cross_sectional_regime_map,
    validate_symbol_regime_alignment,
    validate_regime_transition_signal
)
from usa_signal_bot.core.exceptions import RegimeMapValidationError

@dataclass
class RegimeMapValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeMapValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[RegimeMapValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_timeframe_regime_snapshot_report(item: TimeframeRegimeSnapshot) -> RegimeMapValidationReport:
    issues = []
    try:
        validate_timeframe_regime_snapshot(item)
    except Exception as e:
        issues.append(RegimeMapValidationIssue("ERROR", None, str(e)))
    return _build_report(issues)

def validate_multi_timeframe_confirmation_report(item: MultiTimeframeRegimeConfirmation) -> RegimeMapValidationReport:
    issues = []
    try:
        validate_multi_timeframe_regime_confirmation(item)
    except Exception as e:
         issues.append(RegimeMapValidationIssue("ERROR", None, str(e)))
    return _build_report(issues)

def validate_cross_sectional_regime_map_report(item: CrossSectionalRegimeMap) -> RegimeMapValidationReport:
    issues = []
    try:
        validate_cross_sectional_regime_map(item)
    except Exception as e:
         issues.append(RegimeMapValidationIssue("ERROR", None, str(e)))
    return _build_report(issues)

def validate_symbol_regime_alignment_report(item: SymbolRegimeAlignment) -> RegimeMapValidationReport:
    issues = []
    try:
        validate_symbol_regime_alignment(item)
    except Exception as e:
         issues.append(RegimeMapValidationIssue("ERROR", None, str(e)))
    return _build_report(issues)

def validate_regime_transition_signals_report(items: list[RegimeTransitionSignal]) -> RegimeMapValidationReport:
    issues = []
    for item in items:
        try:
            validate_regime_transition_signal(item)
        except Exception as e:
             issues.append(RegimeMapValidationIssue("ERROR", None, str(e)))
    return _build_report(issues)

def validate_regime_map_review_report(item: RegimeMapReview) -> RegimeMapValidationReport:
    # A shallow check for structural integrity and language
    # Language check
    from usa_signal_bot.regime_map.regime_map_models import regime_map_review_to_dict
    payload = regime_map_review_to_dict(item)

    r1 = validate_no_sensitive_data_in_regime_map_payload(payload)
    r2 = validate_no_broker_execution_fields_in_regime_map(payload)

    issues = r1.issues + r2.issues
    text = json.dumps(payload)
    r3 = validate_no_live_execution_language_in_regime_map(text)
    issues.extend(r3.issues)

    return _build_report(issues)

def validate_no_sensitive_data_in_regime_map_payload(payload: dict[str, Any]) -> RegimeMapValidationReport:
    issues = []
    text = json.dumps(payload).lower()
    suspicious = ["api_key", "secret", "token", "password"]
    for s in suspicious:
        if s in text:
            issues.append(RegimeMapValidationIssue("ERROR", None, f"Sensitive field '{s}' found in payload"))
    return _build_report(issues)

def validate_no_live_execution_language_in_regime_map(text: str) -> RegimeMapValidationReport:
    issues = []
    lower = text.lower()
    banned = [
        "live approved", "sent to broker", "kesin al", "garanti",
        "kesin yükseliş", "kesin düşüş", "kesin kâr"
    ]
    for b in banned:
        if b in lower:
             issues.append(RegimeMapValidationIssue("ERROR", None, f"Banned certainty/live language found: {b}"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_regime_map(payload: dict[str, Any]) -> RegimeMapValidationReport:
    issues = []
    text = json.dumps(payload).lower()
    banned_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for b in banned_fields:
         if b in text:
              issues.append(RegimeMapValidationIssue("ERROR", None, f"Broker execution field found: {b}"))
    return _build_report(issues)

def regime_map_validation_report_to_text(report: RegimeMapValidationReport) -> str:
    text = f"Regime Map Validation: {'VALID' if report.valid else 'INVALID'}\n"
    text += f"Errors: {report.error_count} Warnings: {report.warning_count}\n"
    for iss in report.issues:
        text += f"- [{iss.severity}] {iss.message}\n"
    return text

def assert_regime_map_valid(report: RegimeMapValidationReport) -> None:
    if not report.valid:
        raise RegimeMapValidationError(f"Validation failed: {report.error_count} errors.")

def _build_report(issues: list[RegimeMapValidationIssue]) -> RegimeMapValidationReport:
    err = sum(1 for i in issues if i.severity == "ERROR")
    warn = sum(1 for i in issues if i.severity == "WARNING")
    return RegimeMapValidationReport(
        valid=err == 0,
        issue_count=len(issues),
        warning_count=warn,
        error_count=err,
        blocked_count=err,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )
