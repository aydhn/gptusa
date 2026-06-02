from typing import Any, Dict, List, Optional
from .phase144_models import CalibrationDriftBaseline, DriftBaselineSpec
import uuid
import datetime

def create_calibration_drift_baseline_id() -> str:
    return f"calib_drift_{uuid.uuid4().hex[:12]}"

def build_calibration_drift_baseline(reference_metrics: Dict[str, Any], monitoring_metrics: Dict[str, Any], spec: DriftBaselineSpec) -> CalibrationDriftBaseline:
    return CalibrationDriftBaseline(baseline_id=create_calibration_drift_baseline_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", spec_id=spec.spec_id, reference_ece=None, monitoring_ece=None, ece_shift=None, reference_brier=None, monitoring_brier=None, brier_shift=None, calibration_severity=None, baseline_status=None, threshold_optimization_performed=False, research_data_only=True, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, warnings=[], errors=[], risk_flags=[], metadata={})

def infer_calibration_metric_value(payload: Dict[str, Any], metric_names: List[str]) -> Optional[float]:
    return None

def validate_calibration_drift_baseline(item: CalibrationDriftBaseline) -> List[str]:
    return []

def calibration_drift_summary(item: CalibrationDriftBaseline) -> Dict[str, Any]:
    return {}

def calibration_drift_to_text(item: CalibrationDriftBaseline, limit: int = 300) -> str:
    return "Calibration Drift"
