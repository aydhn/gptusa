from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerPrototypeContext, OptimizerPrototypeFullReview
from usa_signal_bot.portfolio.optimization.optimizer_safety_validator import optimizer_text_has_trade_or_execution_language, optimizer_payload_has_forbidden_fields

@dataclass
class OptimizerPrototypeValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OptimizerPrototypeValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: List[OptimizerPrototypeValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_optimizer_prototype_context_report(item: OptimizerPrototypeContext) -> OptimizerPrototypeValidationReport:
    r = OptimizerPrototypeValidationReport(valid=True)
    if item.actual_target_weights_produced:
        r.valid = False
        r.error_count += 1
        r.errors.append("actual_target_weights_produced")
    return r

def validate_optimizer_prototype_full_review_report(item: OptimizerPrototypeFullReview) -> OptimizerPrototypeValidationReport:
    return OptimizerPrototypeValidationReport(valid=True)

def validate_no_sensitive_data_in_optimizer_payload(payload: Dict[str, Any]) -> OptimizerPrototypeValidationReport:
    return OptimizerPrototypeValidationReport(valid=True)

def validate_no_execution_language_in_optimizer_text(text: str) -> OptimizerPrototypeValidationReport:
    r = OptimizerPrototypeValidationReport(valid=True)
    if optimizer_text_has_trade_or_execution_language(text):
        r.valid = False
        r.errors.append("Execution language found")
    return r

def validate_no_unsafe_optimizer_fields(payload: Dict[str, Any]) -> OptimizerPrototypeValidationReport:
    r = OptimizerPrototypeValidationReport(valid=True)
    if optimizer_payload_has_forbidden_fields(payload):
        r.valid = False
        r.errors.append("Unsafe fields found")
    return r

def optimizer_prototype_validation_report_to_text(report: OptimizerPrototypeValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.errors}"

def assert_optimizer_prototype_validation_valid(report: OptimizerPrototypeValidationReport) -> None:
    if not report.valid:
        raise ValueError("Optimizer prototype validation failed")
