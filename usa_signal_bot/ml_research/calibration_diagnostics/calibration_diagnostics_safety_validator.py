from typing import Any, Dict, List
import pandas as pd

from usa_signal_bot.core.enums import CalibrationDiagnosticsRiskFlag
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationDiagnosticsContext,
    CalibrationCandidateReference,
    CalibrationDiagnosticsReport,
    PostTrainingValidationResult,
    CalibrationGovernanceResult,
    ModelCardCalibrationUpdate,
    CalibrationReadinessGate
)

def validate_calibration_diagnostics_context_safety(context: CalibrationDiagnosticsContext) -> List[str]:
    errs = []
    if context.activation_allowed: errs.append("activation_allowed is true")
    if context.deployment_allowed: errs.append("deployment_allowed is true")
    if context.live_inference_enabled: errs.append("live_inference_enabled is true")
    if context.calibration_fitting_performed: errs.append("calibration_fitting_performed is true")
    if context.produces_trade_signal: errs.append("produces_trade_signal is true")
    return errs

def validate_calibration_candidate_safety(items: List[CalibrationCandidateReference]) -> List[str]:
    return []

def validate_calibration_diagnostics_reports_safety(items: List[CalibrationDiagnosticsReport]) -> List[str]:
    return []

def validate_post_training_validations_safety(items: List[PostTrainingValidationResult]) -> List[str]:
    return []

def validate_calibration_governance_safety(result: CalibrationGovernanceResult) -> List[str]:
    return []

def validate_model_card_calibration_updates_safety(items: List[ModelCardCalibrationUpdate]) -> List[str]:
    return []

def validate_calibration_readiness_gate_safety(gate: CalibrationReadinessGate) -> List[str]:
    return []

def validate_calibration_diagnostics_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return []

def calibration_diagnostics_text_has_trade_or_execution_language(text: str) -> bool:
    unsafe = ["guaranteed profit", "sure bet", "deploy immediately", "send order"]
    text_lower = text.lower()
    return any(u in text_lower for u in unsafe)

def collect_calibration_diagnostics_risk_flags(context: CalibrationDiagnosticsContext = None) -> List[CalibrationDiagnosticsRiskFlag]:
    return []

def calibration_diagnostics_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def calibration_diagnostics_safety_to_text(errors: List[str]) -> str:
    return f"{len(errors)} safety validation errors."
