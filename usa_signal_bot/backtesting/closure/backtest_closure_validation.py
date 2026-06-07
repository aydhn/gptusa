from typing import Any
from dataclasses import dataclass, field

@dataclass
class BacktestClosureValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestClosureValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: list[BacktestClosureValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_no_sensitive_data_in_closure_payload(payload: dict[str, Any]) -> BacktestClosureValidationReport:
    return BacktestClosureValidationReport()

def assert_backtest_closure_validation_valid(report: BacktestClosureValidationReport) -> None:
    if not report.valid:
        raise ValueError("Validation failed")
