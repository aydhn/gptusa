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
    timeframe_regime_snapshot_to_dict,
    multi_timeframe_regime_confirmation_to_dict,
    cross_sectional_regime_map_to_dict,
    symbol_regime_alignment_to_dict,
    regime_transition_signal_to_dict,
    regime_map_review_to_dict
)

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

def _check_broker_fields(payload: dict[str, Any], issues: list[RegimeMapValidationIssue]):
    payload_str = json.dumps(payload)
    bad_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for bf in bad_fields:
        if bf in payload_str:
            issues.append(RegimeMapValidationIssue("ERROR", bf, f"Broker field {bf} found in regime map payload"))

def _check_sensitive_data(payload: dict[str, Any], issues: list[RegimeMapValidationIssue]):
    payload_str = json.dumps(payload).lower()
    bad_keys = ["api_key", "secret", "password", "token"]
    for bk in bad_keys:
        if bk in payload_str:
            issues.append(RegimeMapValidationIssue("ERROR", None, f"Potential sensitive data '{bk}' found in regime map payload"))

def _check_live_execution_language(text: str, issues: list[RegimeMapValidationIssue]):
    text_lower = text.lower()
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "kesin yükseliş", "kesin düşüş", "kesin kâr"]
    for bp in bad_phrases:
         if bp in text_lower:
             issues.append(RegimeMapValidationIssue("ERROR", None, f"Prohibited certainty/live language '{bp}' found"))

def _build_report(issues: list[RegimeMapValidationIssue]) -> RegimeMapValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]

    return RegimeMapValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=1 if errors else 0,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_timeframe_regime_snapshot_report(item: TimeframeRegimeSnapshot) -> RegimeMapValidationReport:
    issues = []
    if not item.symbol:
        issues.append(RegimeMapValidationIssue("ERROR", "symbol", "Symbol cannot be empty"))
    if item.confidence is not None and not ((0.0 <= item.confidence <= 1.0) or (0.0 <= item.confidence <= 100.0)):
        issues.append(RegimeMapValidationIssue("ERROR", "confidence", "Confidence must be 0-1 or 0-100"))

    payload = timeframe_regime_snapshot_to_dict(item)
    _check_broker_fields(payload, issues)
    _check_sensitive_data(payload, issues)
    _check_live_execution_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_multi_timeframe_confirmation_report(item: MultiTimeframeRegimeConfirmation) -> RegimeMapValidationReport:
    issues = []
    if not item.symbol:
        issues.append(RegimeMapValidationIssue("ERROR", "symbol", "Symbol cannot be empty"))

    payload = multi_timeframe_regime_confirmation_to_dict(item)
    _check_broker_fields(payload, issues)
    _check_sensitive_data(payload, issues)
    _check_live_execution_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_cross_sectional_regime_map_report(item: CrossSectionalRegimeMap) -> RegimeMapValidationReport:
    issues = []
    if not item.universe_name:
        issues.append(RegimeMapValidationIssue("ERROR", "universe_name", "Universe name cannot be empty"))
    if item.symbol_count < 0:
        issues.append(RegimeMapValidationIssue("ERROR", "symbol_count", "Symbol count cannot be negative"))

    for count_attr in ["uptrend_count", "downtrend_count", "range_count", "high_vol_count", "thin_liquidity_count", "momentum_positive_count", "momentum_negative_count"]:
        if getattr(item, count_attr) < 0:
            issues.append(RegimeMapValidationIssue("ERROR", count_attr, f"{count_attr} cannot be negative"))

    payload = cross_sectional_regime_map_to_dict(item)
    _check_broker_fields(payload, issues)
    _check_sensitive_data(payload, issues)
    _check_live_execution_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_symbol_regime_alignment_report(item: SymbolRegimeAlignment) -> RegimeMapValidationReport:
    issues = []
    if not item.symbol:
        issues.append(RegimeMapValidationIssue("ERROR", "symbol", "Symbol cannot be empty"))

    payload = symbol_regime_alignment_to_dict(item)
    _check_broker_fields(payload, issues)
    _check_sensitive_data(payload, issues)
    _check_live_execution_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_regime_transition_signals_report(items: list[RegimeTransitionSignal]) -> RegimeMapValidationReport:
    issues = []
    for item in items:
        payload = regime_transition_signal_to_dict(item)
        _check_broker_fields(payload, issues)
        _check_sensitive_data(payload, issues)
        _check_live_execution_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_regime_map_review_report(item: RegimeMapReview) -> RegimeMapValidationReport:
    issues = []
    payload = regime_map_review_to_dict(item)
    _check_broker_fields(payload, issues)
    _check_sensitive_data(payload, issues)
    _check_live_execution_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_no_sensitive_data_in_regime_map_payload(payload: dict[str, Any]) -> RegimeMapValidationReport:
    issues = []
    _check_sensitive_data(payload, issues)
    return _build_report(issues)

def validate_no_live_execution_language_in_regime_map(text: str) -> RegimeMapValidationReport:
     issues = []
     _check_live_execution_language(text, issues)
     return _build_report(issues)

def validate_no_broker_execution_fields_in_regime_map(payload: dict[str, Any]) -> RegimeMapValidationReport:
    issues = []
    _check_broker_fields(payload, issues)
    return _build_report(issues)

def regime_map_validation_report_to_text(report: RegimeMapValidationReport) -> str:
    if report.valid:
        return "Regime Map Validation: PASSED"

    lines = [f"Regime Map Validation: FAILED ({report.error_count} errors, {report.warning_count} warnings)"]
    for i in report.issues:
        lines.append(f"[{i.severity}] {i.field or 'general'}: {i.message}")
    return "\n".join(lines)

def assert_regime_map_valid(report: RegimeMapValidationReport) -> None:
    if not report.valid:
         raise ValueError(f"Regime Map validation failed: {report.errors[0]}")
