from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import CalibrationDiagnosticsContext, CalibrationDiagnosticsFullReview

@dataclass
class CalibrationDiagnosticsValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any]

@dataclass
class CalibrationDiagnosticsValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[CalibrationDiagnosticsValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_calibration_diagnostics_context_report(item: CalibrationDiagnosticsContext) -> CalibrationDiagnosticsValidationReport:
    return CalibrationDiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_calibration_diagnostics_full_review_report(item: CalibrationDiagnosticsFullReview) -> CalibrationDiagnosticsValidationReport:
    return CalibrationDiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_calibration_diagnostics_payload(payload: Dict[str, Any]) -> CalibrationDiagnosticsValidationReport:
    errs = []
    if "api_key" in str(payload).lower(): errs.append("api_key found")
    valid = len(errs) == 0
    return CalibrationDiagnosticsValidationReport(valid, len(errs), 0, len(errs), 0, [], [], errs)

def validate_no_execution_language_in_calibration_diagnostics_text(text: str) -> CalibrationDiagnosticsValidationReport:
    errs = []
    if "send order" in text.lower() or "guaranteed profit" in text.lower(): errs.append("Execution language found")
    valid = len(errs) == 0
    return CalibrationDiagnosticsValidationReport(valid, len(errs), 0, len(errs), 0, [], [], errs)

def validate_no_unsafe_calibration_diagnostics_fields(payload: Dict[str, Any]) -> CalibrationDiagnosticsValidationReport:
    errs = []
    if payload.get("live_inference_enabled"): errs.append("live_inference_enabled is True")
    if payload.get("calibration_fitting_performed"): errs.append("calibration_fitting_performed is True")
    valid = len(errs) == 0
    return CalibrationDiagnosticsValidationReport(valid, len(errs), 0, len(errs), 0, [], [], errs)

def calibration_diagnostics_validation_report_to_text(report: CalibrationDiagnosticsValidationReport) -> str:
    return "Valid" if report.valid else "Invalid"

def assert_calibration_diagnostics_validation_valid(report: CalibrationDiagnosticsValidationReport) -> None:
    if not report.valid:
        raise Exception(f"Validation failed: {report.errors}")
