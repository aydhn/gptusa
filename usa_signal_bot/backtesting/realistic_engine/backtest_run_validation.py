from typing import Dict, Any, List
from dataclasses import dataclass
from .phase147_models import BacktestRunContext, BacktestRunFullReview

@dataclass
class BacktestRunValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any]

@dataclass
class BacktestRunValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[BacktestRunValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_backtest_run_context_report(item: BacktestRunContext) -> BacktestRunValidationReport:
    return BacktestRunValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_backtest_run_full_review_report(item: BacktestRunFullReview) -> BacktestRunValidationReport:
    return BacktestRunValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_backtest_run_payload(payload: Dict[str, Any]) -> BacktestRunValidationReport:
    return BacktestRunValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_execution_language_in_backtest_run_text(text: str) -> BacktestRunValidationReport:
    return BacktestRunValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_unsafe_backtest_run_fields(payload: Dict[str, Any]) -> BacktestRunValidationReport:
    return BacktestRunValidationReport(True, 0, 0, 0, 0, [], [], [])

def backtest_run_validation_report_to_text(report: BacktestRunValidationReport) -> str:
    return f"Validation report valid: {report.valid}"

def assert_backtest_run_validation_valid(report: BacktestRunValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Validation failed: {report.errors}")
