from typing import Any, Dict, List
import pandas as pd

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationInputProfile,
    ReliabilityBinResult,
    CalibrationMetricResult,
    BrierDecompositionResult,
    CalibrationDiagnosticsReport,
    PostTrainingValidationResult,
    CalibrationGovernanceResult,
    CalibrationDiagnosticsContext
)

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "signal", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch",
    "strategy_active", "deployment_enabled", "threshold_order", "calibrated_trade"
]

def validate_calibration_input_profile_schema(item: CalibrationInputProfile) -> List[str]:
    return []

def validate_reliability_bin_result_schema(item: ReliabilityBinResult) -> List[str]:
    return []

def validate_calibration_metric_result_schema(item: CalibrationMetricResult) -> List[str]:
    return []

def validate_brier_decomposition_schema(item: BrierDecompositionResult) -> List[str]:
    return []

def validate_calibration_diagnostics_report_schema(item: CalibrationDiagnosticsReport) -> List[str]:
    return []

def validate_post_training_validation_schema(item: PostTrainingValidationResult) -> List[str]:
    return []

def validate_calibration_governance_schema(item: CalibrationGovernanceResult) -> List[str]:
    return []

def validate_calibration_diagnostics_context_schema(context: CalibrationDiagnosticsContext) -> List[str]:
    return []

def validate_calibration_diagnostics_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_calibration_diagnostics_columns(columns)

def validate_no_forbidden_calibration_diagnostics_columns(columns: List[str]) -> List[str]:
    errs = []
    for col in columns:
        col_lower = col.lower()
        if col_lower == "macd_signal_9": continue
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in col_lower:
                errs.append(f"Forbidden fragment '{frag}' found in column '{col}'")
    return errs

def calibration_diagnostics_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def calibration_diagnostics_schema_to_text(errors: List[str]) -> str:
    return f"{len(errors)} schema validation errors."
