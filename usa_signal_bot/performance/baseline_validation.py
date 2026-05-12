from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.exceptions import PerformanceBaselineValidationError
from usa_signal_bot.performance.baseline_models import PerformanceBaseline, CurrentPerformanceSample, BaselineComparisonResult, PerformanceReviewResult
from usa_signal_bot.performance.threshold_models import SLAEvaluationReport
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult
from usa_signal_bot.performance.alert_rules import PerformanceAlert

@dataclass
class PerformanceValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PerformanceValidationIssue]
    warnings: List[str]
    errors: List[str]

def _check_payload_secrets(payload: Any, path: str = "") -> List[PerformanceValidationIssue]:
    issues = []
    if isinstance(payload, dict):
        for k, v in payload.items():
            curr_path = f"{path}.{k}" if path else k
            if any(sub in k.lower() for sub in ["secret", "token", "api_key", "password"]):
                if not isinstance(v, str) or v != "***REDACTED***":
                    issues.append(PerformanceValidationIssue("ERROR", curr_path, "Potential unredacted secret found."))
            issues.extend(_check_payload_secrets(v, curr_path))
    elif isinstance(payload, list):
        for i, item in enumerate(payload):
            issues.extend(_check_payload_secrets(item, f"{path}[{i}]"))
    return issues

def validate_no_sensitive_data_in_performance_payload(payload: Dict[str, Any]) -> PerformanceValidationReport:
    issues = _check_payload_secrets(payload)
    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "WARNING"),
        error_count=len(errs),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errs
    )

def validate_no_live_execution_language_in_performance(text: str) -> PerformanceValidationReport:
    issues = []
    lower_text = text.lower()
    forbidden = ["live approved", "sent to broker", "kesin al", "garanti", "investment advice"]

    for f in forbidden:
        if f in lower_text:
            issues.append(PerformanceValidationIssue("ERROR", "text_content", f"Forbidden live execution language found: '{f}'"))

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errs),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errs
    )

def validate_no_external_telemetry_fields_in_performance(payload: Dict[str, Any]) -> PerformanceValidationReport:
    issues = []
    forbidden_keys = ["external_endpoint", "telemetry_url", "prometheus", "sentry", "datadog", "newrelic"]

    def _check(data):
        if isinstance(data, dict):
            for k, v in data.items():
                if any(f in k.lower() for f in forbidden_keys):
                    issues.append(PerformanceValidationIssue("ERROR", k, f"Forbidden external telemetry key found: '{k}'"))
                _check(v)
        elif isinstance(data, list):
            for i in data:
                _check(i)

    _check(payload)
    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errs),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errs
    )

def validate_performance_baseline_report(baseline: PerformanceBaseline) -> PerformanceValidationReport:
    from usa_signal_bot.performance.baseline_models import validate_performance_baseline, performance_baseline_to_dict
    issues = []
    try:
        validate_performance_baseline(baseline)
    except PerformanceBaselineValidationError as e:
        issues.append(PerformanceValidationIssue("ERROR", None, str(e)))

    payload = performance_baseline_to_dict(baseline)
    sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
    issues.extend(sec_rep.issues)

    tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
    issues.extend(tel_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)


def validate_current_sample_report(sample: CurrentPerformanceSample) -> PerformanceValidationReport:
    from usa_signal_bot.performance.baseline_models import validate_current_performance_sample, current_performance_sample_to_dict
    issues = []
    try:
        validate_current_performance_sample(sample)
    except PerformanceBaselineValidationError as e:
        issues.append(PerformanceValidationIssue("ERROR", None, str(e)))

    payload = current_performance_sample_to_dict(sample)
    sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
    issues.extend(sec_rep.issues)

    tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
    issues.extend(tel_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)

def validate_baseline_comparison_report(result: BaselineComparisonResult) -> PerformanceValidationReport:
    from usa_signal_bot.performance.baseline_models import validate_baseline_comparison_result, baseline_comparison_result_to_dict
    issues = []
    try:
        validate_baseline_comparison_result(result)
    except PerformanceBaselineValidationError as e:
        issues.append(PerformanceValidationIssue("ERROR", None, str(e)))

    payload = baseline_comparison_result_to_dict(result)
    sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
    issues.extend(sec_rep.issues)

    tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
    issues.extend(tel_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)

def validate_sla_report(report: SLAEvaluationReport) -> PerformanceValidationReport:
    from usa_signal_bot.performance.threshold_models import validate_sla_evaluation_report, sla_evaluation_report_to_dict
    issues = []
    try:
        validate_sla_evaluation_report(report)
    except PerformanceBaselineValidationError as e:
        issues.append(PerformanceValidationIssue("ERROR", None, str(e)))

    payload = sla_evaluation_report_to_dict(report)
    sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
    issues.extend(sec_rep.issues)

    tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
    issues.extend(tel_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)


def validate_performance_gate_report(result: PerformanceAcceptanceGateResult) -> PerformanceValidationReport:
    from usa_signal_bot.performance.acceptance_gate import performance_acceptance_gate_result_to_dict
    issues = []
    payload = performance_acceptance_gate_result_to_dict(result)
    sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
    issues.extend(sec_rep.issues)

    tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
    issues.extend(tel_rep.issues)

    # check actions text for live execution language
    all_text = " ".join(result.required_actions + result.optional_actions)
    text_rep = validate_no_live_execution_language_in_performance(all_text)
    issues.extend(text_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)

def validate_performance_alerts_report(alerts: List[PerformanceAlert]) -> PerformanceValidationReport:
    from usa_signal_bot.performance.alert_rules import performance_alert_to_dict
    issues = []
    for alert in alerts:
        payload = performance_alert_to_dict(alert)
        sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
        issues.extend(sec_rep.issues)

        tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
        issues.extend(tel_rep.issues)

        text_rep = validate_no_live_execution_language_in_performance(alert.title + " " + alert.message)
        issues.extend(text_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)

def validate_performance_review_report(result: PerformanceReviewResult) -> PerformanceValidationReport:
    from usa_signal_bot.performance.baseline_models import performance_review_result_to_dict
    issues = []
    payload = performance_review_result_to_dict(result)
    sec_rep = validate_no_sensitive_data_in_performance_payload(payload)
    issues.extend(sec_rep.issues)

    tel_rep = validate_no_external_telemetry_fields_in_performance(payload)
    issues.extend(tel_rep.issues)

    errs = [i.message for i in issues if i.severity == "ERROR"]
    return PerformanceValidationReport(len(errs) == 0, len(issues), sum(1 for i in issues if i.severity == "WARNING"), len(errs), 0, issues, [], errs)


def performance_validation_report_to_text(report: PerformanceValidationReport) -> str:
    lines = [f"Performance Validation Report [Valid: {report.valid}]"]
    lines.append(f"Issues: {report.issue_count} (Warn: {report.warning_count}, Err: {report.error_count})")
    for i in report.issues:
        field_str = f" [{i.field}]" if i.field else ""
        lines.append(f" - {i.severity}{field_str}: {i.message}")
    return "\n".join(lines)

def assert_performance_valid(report: PerformanceValidationReport) -> None:
    if not report.valid:
        raise PerformanceBaselineValidationError(f"Performance validation failed: {report.error_count} errors found.")
