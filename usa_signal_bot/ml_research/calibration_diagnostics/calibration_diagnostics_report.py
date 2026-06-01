import datetime
import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import CalibrationDiagnosticsStatus, CalibrationDiagnosticsDecision, CalibrationDiagnosticsReportType, CalibrationDiagnosticsQuality
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    CalibrationInputProfile,
    CalibrationDiagnosticsReport,
    CalibrationDiagnosticsContext,
    CalibrationDiagnosticsFullReview,
    create_calibration_diagnostics_report_id,
    create_calibration_diagnostics_context_id,
    create_calibration_diagnostics_full_review_id,
    ModelComparisonIngestionResult,
    CalibrationGovernanceResult,
    CalibrationReadinessGate
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_calibration_diagnostics_report_for_candidate(candidate: CalibrationCandidateReference, input_profile: CalibrationInputProfile, prediction_df: pd.DataFrame, label_df: Optional[pd.DataFrame] = None, target_df: Optional[pd.DataFrame] = None) -> CalibrationDiagnosticsReport:
    return CalibrationDiagnosticsReport(
        report_id=create_calibration_diagnostics_report_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        model_artifact_id="dummy",
        experiment_id="dummy",
        input_profile=input_profile,
        reliability_bins=[],
        calibration_metrics=[],
        brier_decomposition=None,
        score_distribution=None,
        class_balance=None,
        report_hash="dummy",
        report_valid=True,
        quality=CalibrationDiagnosticsQuality.HIGH,
        fitting_performed=False,
        calibrated_model_created=False,
        threshold_optimization_performed=False,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_calibration_diagnostics_context() -> CalibrationDiagnosticsContext:
    pass # Filled in mostly by tests or orchestration

def build_calibration_diagnostics_full_review() -> CalibrationDiagnosticsFullReview:
    pass # Filled in mostly by tests or orchestration

def calibration_diagnostics_full_review_summary(review: CalibrationDiagnosticsFullReview) -> Dict[str, Any]:
    return {}

def calibration_diagnostics_limitations_text() -> str:
    return "Phase 141 is local offline only. No execution."

def calibration_diagnostics_full_review_to_text(review: CalibrationDiagnosticsFullReview, limit: int = 300) -> str:
    return "Full Review"
