from typing import Any, Dict, List, Optional
try:
    import pandas
except ImportError:
    pandas = None
from .phase144_models import PredictionDriftBaseline, DriftBaselineSpec
import uuid
import datetime

def create_prediction_drift_baseline_id() -> str:
    return f"pred_drift_{uuid.uuid4().hex[:12]}"

def build_prediction_drift_baseline(reference_df: Any, monitoring_df: Any, spec: DriftBaselineSpec) -> PredictionDriftBaseline:
    return PredictionDriftBaseline(baseline_id=create_prediction_drift_baseline_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", spec_id=spec.spec_id, prototype_id=None, prediction_columns=[], reference_summary={}, monitoring_summary={}, metric_values={}, drift_severity=None, baseline_status=None, row_count_reference=0, row_count_monitoring=0, research_data_only=True, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, warnings=[], errors=[], risk_flags=[], metadata={})

def summarize_prediction_columns(df: Any, prediction_columns: List[str]) -> Dict[str, Any]:
    return {}

def calculate_prediction_shift_metrics(reference_summary: Dict[str, Any], monitoring_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {}

def validate_prediction_drift_baseline(item: PredictionDriftBaseline) -> List[str]:
    return []

def prediction_drift_baseline_summary(item: PredictionDriftBaseline) -> Dict[str, Any]:
    return {}

def prediction_drift_baseline_to_text(item: PredictionDriftBaseline, limit: int = 300) -> str:
    return "Prediction Drift"
