from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

from usa_signal_bot.regression.regression_models import RegressionRunResult, ReleaseRehearsalResult, ReleaseCandidateStatus
from usa_signal_bot.core.exceptions import RegressionValidationError

@dataclass
class RegressionValidationIssue:
    severity: str
    message: str
    field_name: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegressionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[RegressionValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def validate_regression_run_result_report(result: RegressionRunResult) -> RegressionValidationReport:
    report = RegressionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0)

    for step in result.step_results:
        if step.duration_seconds is not None and step.duration_seconds < 0:
            report.errors.append(f"Negative duration in step {step.step_name.value}")

    _add_counts(report)
    return report

def validate_release_rehearsal_result_report(result: ReleaseRehearsalResult) -> RegressionValidationReport:
    report = RegressionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0)

    if result.status == ReleaseCandidateStatus.PASSED and result.failed_steps > 0:
        report.errors.append("Status PASSED but has failed steps")

    _add_counts(report)
    return report

def validate_golden_dataset_files(base_dir: Path) -> RegressionValidationReport:
    report = RegressionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0)

    required = ["manifest.json", "signals.jsonl", "candidates.jsonl", "risk_decisions.jsonl", "allocations.jsonl"]
    for r in required:
        if not (base_dir / r).exists():
            report.errors.append(f"Missing required golden file: {r}")

    _add_counts(report)
    return report

def validate_snapshot_comparison_payload(payload: Dict[str, Any]) -> RegressionValidationReport:
    report = RegressionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0)
    status = payload.get("status")
    if status == "INVALID":
        report.errors.append(f"Snapshot comparison is INVALID: {payload.get('message')}")
    elif status not in ["MATCH", "DRIFT", "MISSING_BASELINE", "MISSING_CURRENT", "SKIPPED"]:
        report.warnings.append(f"Unknown snapshot comparison status: {status}")

    _add_counts(report)
    return report

def validate_no_live_execution_in_regression(payload: Dict[str, Any]) -> RegressionValidationReport:
    report = RegressionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0)
    s_payload = str(payload).lower()

    forbidden = ["live_order", "broker_order", "demo_order", "send_to_broker"]
    for f in forbidden:
        if f in s_payload:
            report.errors.append(f"Forbidden execution field found: {f}")

    _add_counts(report)
    return report

def validate_no_investment_advice_language_in_regression(text: str) -> RegressionValidationReport:
    report = RegressionValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0)
    lower_text = text.lower()

    forbidden = ["kesin al", "kesin sat", "garanti", "live approved", "investment advice"]
    for f in forbidden:
        if f in lower_text:
            report.errors.append(f"Forbidden advice language found: '{f}'")

    _add_counts(report)
    return report

def regression_validation_report_to_text(report: RegressionValidationReport) -> str:
    lines = [
        f"Validation Report (Valid: {report.valid})",
        f"Errors: {report.error_count}, Warnings: {report.warning_count}"
    ]
    for e in report.errors:
        lines.append(f"[ERROR] {e}")
    for w in report.warnings:
        lines.append(f"[WARN] {w}")
    return "\n".join(lines)

def assert_regression_valid(report: RegressionValidationReport) -> None:
    if not report.valid:
        raise RegressionValidationError(regression_validation_report_to_text(report))

def _add_counts(report: RegressionValidationReport):
    report.error_count = len(report.errors)
    report.warning_count = len(report.warnings)
    report.issue_count = report.error_count + report.warning_count
    report.valid = report.error_count == 0
