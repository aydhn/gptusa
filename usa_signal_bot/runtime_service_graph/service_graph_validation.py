from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraph,
    SafeOrchestrationPlan,
    OrchestrationDryRunResult,
    RuntimeServiceGraphFullReview
)
from usa_signal_bot.core.exceptions import ServiceGraphValidationError

@dataclass
class RuntimeServiceGraphValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeServiceGraphValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RuntimeServiceGraphValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _create_report(issues: List[RuntimeServiceGraphValidationIssue]) -> RuntimeServiceGraphValidationReport:
    errors = [i.message for i in issues if i.severity in ("ERROR", "BLOCKED")]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    blocked = [i for i in issues if i.severity == "BLOCKED"]

    return RuntimeServiceGraphValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_runtime_service_graph_report(graph: RuntimeServiceGraph) -> RuntimeServiceGraphValidationReport:
    issues = []
    if graph.activation_allowed:
        issues.append(RuntimeServiceGraphValidationIssue("BLOCKED", "activation_allowed", "Must be false"))
    if graph.broker_execution_enabled:
        issues.append(RuntimeServiceGraphValidationIssue("BLOCKED", "broker_execution_enabled", "Must be false"))
    return _create_report(issues)

def validate_orchestration_plan_report(plan: SafeOrchestrationPlan) -> RuntimeServiceGraphValidationReport:
    issues = []
    if plan.execution_allowed:
        issues.append(RuntimeServiceGraphValidationIssue("BLOCKED", "execution_allowed", "Must be false"))
    return _create_report(issues)

def validate_orchestration_dry_run_report(result: OrchestrationDryRunResult) -> RuntimeServiceGraphValidationReport:
    issues = []
    if result.execution_performed:
        issues.append(RuntimeServiceGraphValidationIssue("BLOCKED", "execution_performed", "Must be false"))
    return _create_report(issues)

def validate_runtime_service_graph_full_review_report(review: RuntimeServiceGraphFullReview) -> RuntimeServiceGraphValidationReport:
    issues = []
    return _create_report(issues)

def validate_no_sensitive_data_in_service_graph_payload(payload: Dict[str, Any]) -> RuntimeServiceGraphValidationReport:
    issues = []
    text = json.dumps(payload).lower()
    for bad in ["api_key", "secret", "token", "password", "broker_order_id"]:
        if bad in text:
            issues.append(RuntimeServiceGraphValidationIssue("ERROR", None, f"Found blocked term: {bad}"))
    return _create_report(issues)

def validate_no_execution_language_in_service_graph_text(text: str) -> RuntimeServiceGraphValidationReport:
    issues = []
    text_lower = text.lower()
    for bad in ["emir gönder", "aktif trading", "paper'a alın", "kesin al", "garanti"]:
        if bad in text_lower:
            issues.append(RuntimeServiceGraphValidationIssue("ERROR", None, f"Found execution language: {bad}"))
    return _create_report(issues)

def service_graph_validation_report_to_text(report: RuntimeServiceGraphValidationReport) -> str:
    return f"Report valid: {report.valid}. Errors: {report.error_count}"

def assert_service_graph_valid(report: RuntimeServiceGraphValidationReport) -> None:
    if not report.valid:
        raise ServiceGraphValidationError(f"Validation failed: {report.errors}")
