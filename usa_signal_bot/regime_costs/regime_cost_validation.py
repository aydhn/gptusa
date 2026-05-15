import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostMultiplier, RegimeCostCurveSelection,
    AdaptiveExecutionRealismDecision, RegimeAwareCostBreakdown, RegimeCostReview
)

@dataclass
class RegimeCostValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCostValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RegimeCostValidationIssue]
    warnings: List[str]
    errors: List[str]

def _check_payload_for_forbidden(payload: Any) -> List[str]:
    s = json.dumps(payload).lower()
    errs = []
    forbidden_keys = ["api_key", "secret", "password", "token", "broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    forbidden_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "guaranteed fill", "kesin maliyet", "kesin kâr"]

    for fk in forbidden_keys:
        if f'"{fk}"' in s:
            errs.append(f"Forbidden key found: {fk}")
    for fp in forbidden_phrases:
        if fp in s:
            errs.append(f"Forbidden phrase found: {fp}")

    return errs

def _build_report(errs: List[str]) -> RegimeCostValidationReport:
    issues = [RegimeCostValidationIssue(severity="ERROR", field=None, message=e) for e in errs]
    return RegimeCostValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=len(errs),
        issues=issues,
        warnings=[],
        errors=errs
    )

def validate_cost_regime_snapshot_report(item: CostRegimeSnapshot) -> RegimeCostValidationReport:
    errs = []
    if not item.symbol:
        errs.append("Symbol empty")
    return _build_report(errs)

def validate_regime_cost_multiplier_report(item: RegimeCostMultiplier) -> RegimeCostValidationReport:
    errs = []
    if item.combined_multiplier < 0:
        errs.append("Negative multiplier")
    return _build_report(errs)

def validate_regime_cost_curve_selection_report(item: RegimeCostCurveSelection) -> RegimeCostValidationReport:
    errs = []
    if not item.symbol:
        errs.append("Symbol empty")
    return _build_report(errs)

def validate_adaptive_execution_decision_report(item: AdaptiveExecutionRealismDecision) -> RegimeCostValidationReport:
    errs = []
    if not item.symbol:
        errs.append("Symbol empty")
    return _build_report(errs)

def validate_regime_aware_cost_breakdown_report(item: RegimeAwareCostBreakdown) -> RegimeCostValidationReport:
    errs = []
    if not item.symbol:
        errs.append("Symbol empty")
    return _build_report(errs)

def validate_regime_cost_review_report(item: RegimeCostReview) -> RegimeCostValidationReport:
    errs = []
    if not item.review_id:
        errs.append("Review ID empty")
    return _build_report(errs)

def validate_no_sensitive_data_in_regime_cost_payload(payload: Dict[str, Any]) -> RegimeCostValidationReport:
    return _build_report(_check_payload_for_forbidden(payload))

def validate_no_live_execution_language_in_regime_cost(text: str) -> RegimeCostValidationReport:
    errs = []
    forbidden_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "guaranteed fill", "kesin maliyet", "kesin kâr"]
    s = text.lower()
    for fp in forbidden_phrases:
        if fp in s:
            errs.append(f"Forbidden phrase found: {fp}")
    return _build_report(errs)

def validate_no_broker_execution_fields_in_regime_cost(payload: Dict[str, Any]) -> RegimeCostValidationReport:
    return _build_report(_check_payload_for_forbidden(payload))

def regime_cost_validation_report_to_text(report: RegimeCostValidationReport) -> str:
    res = "VALID" if report.valid else "INVALID"
    return f"Regime Cost Validation: {res} ({report.error_count} errors)"

def assert_regime_cost_valid(report: RegimeCostValidationReport) -> None:
    if not report.valid:
        raise Exception(f"Regime cost validation failed: {report.errors}")
