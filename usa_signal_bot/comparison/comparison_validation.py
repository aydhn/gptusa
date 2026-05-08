from dataclasses import dataclass, field
from typing import Any, List, Optional
import json

from usa_signal_bot.core.exceptions import ComparisonValidationError
from usa_signal_bot.comparison.comparison_models import (
    ComparisonRunRequest, ComparisonRunResult, MatchedTradePair,
    PerformanceGapMetrics, ExecutionGapMetrics, SignalDriftMetrics
)

@dataclass
class ComparisonValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict = field(default_factory=dict)

@dataclass
class ComparisonValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[ComparisonValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_comparison_run_request_report(request: ComparisonRunRequest) -> ComparisonValidationReport:
    issues = []

    if not request.request_id:
        issues.append(ComparisonValidationIssue("ERROR", "request_id", "Request ID cannot be empty"))

    has_paper = bool(request.paper_run_id or request.paper_run_dir)
    has_backtest = bool(request.backtest_run_id or request.backtest_run_dir or request.basket_run_id or request.basket_run_dir)
    has_scan = bool(request.scan_run_id or request.scan_run_dir or request.signal_file or request.candidate_file)

    if not (has_paper and has_backtest) and not has_scan:
        issues.append(ComparisonValidationIssue("ERROR", "sources", "Must provide either (paper + backtest) or scan/signal sources"))

    return _build_report(issues)

def validate_comparison_run_result_report(result: ComparisonRunResult) -> ComparisonValidationReport:
    issues = []

    if not result.run_id:
        issues.append(ComparisonValidationIssue("ERROR", "run_id", "Run ID cannot be empty"))

    # Execution constraints
    no_exec_report = validate_no_execution_in_comparison(result)
    issues.extend(no_exec_report.issues)

    return _build_report(issues)

def validate_matched_trades_report(pairs: List[MatchedTradePair]) -> ComparisonValidationReport:
    issues = []
    for i, p in enumerate(pairs):
        if not p.match_id:
            issues.append(ComparisonValidationIssue("ERROR", f"pairs[{i}].match_id", "Match ID cannot be empty"))
    return _build_report(issues)

def validate_performance_gap_report(metrics: PerformanceGapMetrics) -> ComparisonValidationReport:
    issues = []
    if metrics.total_return_gap_pct is not None and abs(metrics.total_return_gap_pct) == float('inf'):
        issues.append(ComparisonValidationIssue("ERROR", "total_return_gap_pct", "Gap percentage cannot be infinite"))
    return _build_report(issues)

def validate_execution_gap_report(metrics: ExecutionGapMetrics) -> ComparisonValidationReport:
    issues = []
    if metrics.execution_realism_score is not None:
        if not (0.0 <= metrics.execution_realism_score <= 100.0):
            issues.append(ComparisonValidationIssue("ERROR", "execution_realism_score", "Realism score must be between 0 and 100"))
    return _build_report(issues)

def validate_signal_drift_report(metrics: Optional[SignalDriftMetrics]) -> ComparisonValidationReport:
    issues = []
    if metrics and metrics.compared_signal_count < 0:
        issues.append(ComparisonValidationIssue("ERROR", "compared_signal_count", "Count cannot be negative"))
    return _build_report(issues)

def validate_no_execution_in_comparison(result: ComparisonRunResult) -> ComparisonValidationReport:
    issues = []
    from usa_signal_bot.comparison.comparison_models import comparison_run_result_to_dict
    data = comparison_run_result_to_dict(result)

    # Deep search for broker terms
    s = json.dumps(data).lower()
    for term in ["broker_order", "live_order", "demo_order", "paper_order_to_send"]:
        if term in s:
            issues.append(ComparisonValidationIssue("ERROR", "execution_guard", f"Result contains execution-related term: {term}"))

    return _build_report(issues)

def validate_no_investment_advice_language_in_comparison(text: str) -> ComparisonValidationReport:
    issues = []
    t = text.lower()
    for term in ["kesin al", "kesin sat", "garanti", "investment advice", "buy now"]:
        if term in t:
            issues.append(ComparisonValidationIssue("ERROR", "advice_guard", f"Text contains forbidden advice term: {term}"))
    return _build_report(issues)

def comparison_validation_report_to_text(report: ComparisonValidationReport) -> str:
    lines = [f"Comparison Validation Report (Valid: {report.valid})"]
    lines.append(f"Errors: {report.error_count}, Warnings: {report.warning_count}")
    for i in report.issues:
        lines.append(f"  [{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_comparison_valid(report: ComparisonValidationReport) -> None:
    if not report.valid:
        raise ComparisonValidationError(f"Comparison validation failed with {report.error_count} errors: {report.issues[0].message if report.issues else 'Unknown'}")

def _build_report(issues: List[ComparisonValidationIssue]) -> ComparisonValidationReport:
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]
    return ComparisonValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors]
    )
