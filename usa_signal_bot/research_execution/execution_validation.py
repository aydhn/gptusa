from dataclasses import dataclass, field
from typing import Any
import json

from usa_signal_bot.research_execution.execution_models import (
    ConfigSnapshot, ExperimentRunContext, ResearchRun,
    ExperimentComparisonReport, ResearchExecutionReview
)
from usa_signal_bot.core.exceptions import ResearchExecutionValidationError

@dataclass
class ResearchExecutionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchExecutionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ResearchExecutionValidationIssue]
    warnings: list[str]
    errors: list[str]

def _create_report(issues: list[ResearchExecutionValidationIssue]) -> ResearchExecutionValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = len([i for i in issues if i.severity == "BLOCKED"])
    return ResearchExecutionValidationReport(
        valid=len(errors) == 0 and blocked == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=blocked,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_config_snapshot_report(item: ConfigSnapshot) -> ResearchExecutionValidationReport:
    issues = []
    r = validate_no_sensitive_data_in_execution_payload(item.config_payload)
    issues.extend(r.issues)
    return _create_report(issues)

def validate_run_context_report(item: ExperimentRunContext) -> ResearchExecutionValidationReport:
    issues = []
    if item.allowed_to_modify_config:
        issues.append(ResearchExecutionValidationIssue("ERROR", "allowed_to_modify_config", "MUST be False"))
    if item.allowed_to_send_orders:
        issues.append(ResearchExecutionValidationIssue("ERROR", "allowed_to_send_orders", "MUST be False"))
    return _create_report(issues)

def validate_research_run_report(item: ResearchRun) -> ResearchExecutionValidationReport:
    issues = []
    if item.context:
        r = validate_run_context_report(item.context)
        issues.extend(r.issues)

    txt = json.dumps(item.metrics)
    r2 = validate_no_live_execution_language_in_execution(txt)
    issues.extend(r2.issues)
    return _create_report(issues)

def validate_comparison_report_report(item: ExperimentComparisonReport) -> ResearchExecutionValidationReport:
    issues = []
    txt = json.dumps(item.summary)
    r2 = validate_no_live_execution_language_in_execution(txt)
    r3 = validate_no_auto_apply_or_optimizer_language(txt)
    issues.extend(r2.issues)
    issues.extend(r3.issues)
    return _create_report(issues)

def validate_research_execution_review_report(item: ResearchExecutionReview) -> ResearchExecutionValidationReport:
    issues = []
    for run in item.runs:
        issues.extend(validate_research_run_report(run).issues)
    for cr in item.comparison_reports:
        issues.extend(validate_comparison_report_report(cr).issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_execution_payload(payload: dict[str, Any]) -> ResearchExecutionValidationReport:
    issues = []
    txt = json.dumps(payload).lower()
    for t in ["api_key", "secret", "password"]:
        if f'"{t}"' in txt and "[redacted]" not in txt:
             pass
    def check_dict(d):
        for k, v in d.items():
            if isinstance(v, dict): check_dict(v)
            elif isinstance(v, str):
                if any(sec in k.lower() for sec in ["api_key", "secret", "password"]) and v != "[REDACTED]":
                    issues.append(ResearchExecutionValidationIssue("ERROR", k, f"Unredacted secret found: {k}"))
    check_dict(payload)
    return _create_report(issues)

def validate_no_live_execution_language_in_execution(text: str) -> ResearchExecutionValidationReport:
    issues = []
    t = text.lower()
    bad_terms = ["live approved", "sent to broker", "kesin al", "garanti"]
    for bt in bad_terms:
        if bt in t:
            issues.append(ResearchExecutionValidationIssue("ERROR", None, f"Found prohibited live execution language: {bt}"))
    return _create_report(issues)

def validate_no_auto_apply_or_optimizer_language(text: str) -> ResearchExecutionValidationReport:
    issues = []
    t = text.lower()
    bad_terms = ["otomatik optimize et", "parametreyi otomatik değiştir", "production'a geçir", "kesin uygula", "kesin kâr"]
    for bt in bad_terms:
        if bt in t:
            issues.append(ResearchExecutionValidationIssue("ERROR", None, f"Found prohibited auto optimization language: {bt}"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_execution(payload: dict[str, Any]) -> ResearchExecutionValidationReport:
    issues = []
    def check_dict(d):
        for k, v in d.items():
            if isinstance(v, dict): check_dict(v)
            elif k in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
                issues.append(ResearchExecutionValidationIssue("ERROR", k, f"Found prohibited broker execution field: {k}"))
    check_dict(payload)
    return _create_report(issues)

def research_execution_validation_report_to_text(report: ResearchExecutionValidationReport) -> str:
    lines = [f"--- EXECUTION VALIDATION: {'VALID' if report.valid else 'INVALID'} ---"]
    lines.append(f"Issues: {report.issue_count} (Errors: {report.error_count}, Warnings: {report.warning_count})")
    for i in report.issues:
        lines.append(f"  [{i.severity}] {i.field or 'Global'}: {i.message}")
    return "\n".join(lines)

def assert_research_execution_valid(report: ResearchExecutionValidationReport) -> None:
    if not report.valid:
        raise ResearchExecutionValidationError(f"Execution validation failed: {report.errors}")
