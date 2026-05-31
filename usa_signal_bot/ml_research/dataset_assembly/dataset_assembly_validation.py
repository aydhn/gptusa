from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetAssemblyContext,
    MLDatasetAssemblyFullReview
)
from usa_signal_bot.ml_research.dataset_assembly.dataset_assembly_safety_validator import (
    dataset_assembly_text_has_trade_or_execution_language,
    validate_dataset_assembly_context_safety
)

@dataclass
class MLDatasetAssemblyValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLDatasetAssemblyValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[MLDatasetAssemblyValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _add_issue(report: MLDatasetAssemblyValidationReport, severity: str, fld: Optional[str], msg: str):
    report.issues.append(MLDatasetAssemblyValidationIssue(severity=severity, field=fld, message=msg))
    report.issue_count += 1
    if severity == "WARNING":
        report.warning_count += 1
        report.warnings.append(msg)
    elif severity == "ERROR":
        report.error_count += 1
        report.errors.append(msg)
    elif severity == "BLOCKED":
        report.blocked_count += 1
        report.errors.append(msg)
        report.valid = False

def validate_dataset_assembly_context_report(item: MLDatasetAssemblyContext) -> MLDatasetAssemblyValidationReport:
    r = MLDatasetAssemblyValidationReport(valid=True)
    errors = validate_dataset_assembly_context_safety(item)
    for e in errors:
        _add_issue(r, "BLOCKED", None, e)
    return r

def validate_dataset_assembly_full_review_report(item: MLDatasetAssemblyFullReview) -> MLDatasetAssemblyValidationReport:
    r = MLDatasetAssemblyValidationReport(valid=True)
    if not item.readiness_gate or not item.readiness_gate.ready_for_phase138:
        _add_issue(r, "WARNING", "readiness_gate", "Review is not ready for Phase 138")
    if item.context:
        ctx_r = validate_dataset_assembly_context_report(item.context)
        for iss in ctx_r.issues:
            _add_issue(r, iss.severity, iss.field, iss.message)
    return r

def validate_no_sensitive_data_in_dataset_assembly_payload(payload: Dict[str, Any]) -> MLDatasetAssemblyValidationReport:
    r = MLDatasetAssemblyValidationReport(valid=True)
    payload_str = json.dumps(payload).lower()
    for s in ["api_key", "secret", "password", "token", "private_key"]:
        if s in payload_str:
            _add_issue(r, "BLOCKED", None, f"Potential sensitive data found: {s}")
    return r

def validate_no_execution_language_in_dataset_assembly_text(text: str) -> MLDatasetAssemblyValidationReport:
    r = MLDatasetAssemblyValidationReport(valid=True)
    if dataset_assembly_text_has_trade_or_execution_language(text):
        _add_issue(r, "BLOCKED", None, "Execution or trading language found in text")
    return r

def validate_no_unsafe_dataset_assembly_fields(payload: Dict[str, Any]) -> MLDatasetAssemblyValidationReport:
    r = MLDatasetAssemblyValidationReport(valid=True)
    unsafe = ["activation_allowed", "deployment_allowed", "active_paper_enabled", "broker_execution_enabled", "produces_trade_signal", "model_training_used"]
    for u in unsafe:
        if payload.get(u) is True:
            _add_issue(r, "BLOCKED", u, f"Forbidden field {u} is True")
    return r

def dataset_assembly_validation_report_to_text(report: MLDatasetAssemblyValidationReport) -> str:
    return json.dumps({
        "valid": report.valid,
        "blocked_count": report.blocked_count,
        "error_count": report.error_count,
        "warning_count": report.warning_count,
        "errors": report.errors
    }, indent=2)

def assert_dataset_assembly_validation_valid(report: MLDatasetAssemblyValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Dataset assembly validation failed: {report.errors}")
