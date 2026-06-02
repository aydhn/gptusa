from typing import Any, Dict, List, Optional
from .phase144_models import *
import uuid
import datetime
import math
import statistics

def create_drift_metric_result_id() -> str:
    return f"drift_metric_{uuid.uuid4().hex[:12]}"

def build_drift_metric_results(feature: Optional[FeatureDriftBaseline] = None, prediction: Optional[PredictionDriftBaseline] = None, score: Optional[ScoreDistributionDriftBaseline] = None, calibration: Optional[CalibrationDriftBaseline] = None, residual: Optional[ResidualDriftBaseline] = None, label: Optional[LabelDistributionDriftBaseline] = None, regime: Optional[RegimeDriftBaseline] = None) -> List[DriftMetricResult]:
    results = []

    if feature and feature.metric_values:
        for feat_name, shift_val in feature.metric_values.items():
            results.append(DriftMetricResult(
                metric_result_id=create_drift_metric_result_id(),
                created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
                baseline_kind=DriftBaselineKind.FEATURE_DRIFT,
                metric_kind=DriftMetricKind.MEAN_SHIFT,
                metric_name=f"{feat_name}_mean_shift",
                prototype_id=None,
                value=shift_val,
                severity=infer_drift_severity(shift_val, DriftMetricKind.MEAN_SHIFT),
                status=DriftBaselineStatus.VALID,
                sample_count_reference=feature.row_count_reference,
                sample_count_monitoring=feature.row_count_monitoring,
                diagnostic_notes=[f"Calculated mean shift for {feat_name}"],
                non_trading_metric=True,
                research_data_only=True,
                investment_advice=False,
                produces_trade_signal=False,
                produces_order_decision=False,
                produces_portfolio_weights=False,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            ))

    return results

def infer_drift_severity(value: Optional[float], metric_kind: DriftMetricKind) -> DriftSeverity:
    if value is None:
        return DriftSeverity.UNKNOWN
    val = abs(value)
    if val < 0.1:
        return DriftSeverity.LOW
    elif val < 0.3:
        return DriftSeverity.MEDIUM
    elif val < 0.5:
        return DriftSeverity.HIGH
    else:
        return DriftSeverity.BLOCKING

def calculate_mean_shift(reference_values: List[float], monitoring_values: List[float]) -> Optional[float]:
    if not reference_values or not monitoring_values:
        return None
    ref_mean = statistics.mean(reference_values)
    mon_mean = statistics.mean(monitoring_values)
    if ref_mean == 0:
        return mon_mean if mon_mean == 0 else float('inf')
    return (mon_mean - ref_mean) / abs(ref_mean)

def calculate_std_shift(reference_values: List[float], monitoring_values: List[float]) -> Optional[float]:
    if len(reference_values) < 2 or len(monitoring_values) < 2:
        return None
    ref_std = statistics.stdev(reference_values)
    mon_std = statistics.stdev(monitoring_values)
    if ref_std == 0:
        return mon_std if mon_std == 0 else float('inf')
    return (mon_std - ref_std) / abs(ref_std)

def calculate_distribution_overlap_approx(reference_values: List[float], monitoring_values: List[float]) -> Optional[float]:
    # Placeholder for overlap approximation. Returns the ratio of common range.
    if not reference_values or not monitoring_values:
        return None
    ref_min, ref_max = min(reference_values), max(reference_values)
    mon_min, mon_max = min(monitoring_values), max(monitoring_values)

    overlap_min = max(ref_min, mon_min)
    overlap_max = min(ref_max, mon_max)

    if overlap_max <= overlap_min:
        return 0.0

    ref_range = ref_max - ref_min
    if ref_range == 0:
        return 1.0 if overlap_max > overlap_min else 0.0

    return (overlap_max - overlap_min) / ref_range

def validate_drift_metric_results(items: List[DriftMetricResult]) -> List[str]:
    errs = []
    for item in items:
        if not item.non_trading_metric:
            errs.append("Metric must be flagged as non-trading.")
    return errs

def drift_metric_results_summary(items: List[DriftMetricResult]) -> Dict[str, Any]:
    return {"total": len(items)}

def drift_metric_results_to_text(items: List[DriftMetricResult], limit: int = 300) -> str:
    return f"Calculated {len(items)} drift metrics."
