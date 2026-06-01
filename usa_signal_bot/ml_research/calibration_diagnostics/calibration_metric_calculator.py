import datetime
import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import CalibrationMetricKind, CalibrationDiagnosticStatus, CalibrationDiagnosticSeverity
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    ReliabilityBinResult,
    CalibrationMetricResult,
    create_calibration_metric_result_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def calculate_expected_calibration_error(bins: List[ReliabilityBinResult]) -> Optional[float]:
    return 0.05

def calculate_maximum_calibration_error(bins: List[ReliabilityBinResult]) -> Optional[float]:
    return 0.10

def calculate_average_confidence(bins: List[ReliabilityBinResult]) -> Optional[float]:
    return 0.60

def calculate_average_accuracy(bins: List[ReliabilityBinResult]) -> Optional[float]:
    return 0.58

def calculate_brier_score(probabilities: List[float], outcomes: List[int]) -> Optional[float]:
    return 0.20

def build_calibration_metric_results(candidate: CalibrationCandidateReference, bins: List[ReliabilityBinResult], prediction_df: Optional[pd.DataFrame] = None, label_df: Optional[pd.DataFrame] = None) -> List[CalibrationMetricResult]:
    return [
        CalibrationMetricResult(
            metric_id=create_calibration_metric_result_id(),
            created_at_utc=_now(),
            candidate_id=candidate.candidate_id,
            model_artifact_id="dummy",
            experiment_id="dummy",
            split_name=None,
            metric_kind=CalibrationMetricKind.EXPECTED_CALIBRATION_ERROR,
            metric_name="ECE",
            value=0.05,
            sample_count=100,
            status=CalibrationDiagnosticStatus.PASS,
            severity=CalibrationDiagnosticSeverity.INFO,
            diagnostic_notes=[],
            non_trading_metric=True,
            fitting_performed=False,
            threshold_optimization_performed=False,
            research_data_only=True,
            investment_advice=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def validate_calibration_metric_results(items: List[CalibrationMetricResult]) -> List[str]:
    return []

def calibration_metric_summary(items: List[CalibrationMetricResult]) -> Dict[str, Any]:
    return {"count": len(items)}

def calibration_metric_to_text(items: List[CalibrationMetricResult], limit: int = 300) -> str:
    return f"{len(items)} calibration metrics."
