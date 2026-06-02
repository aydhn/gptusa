from typing import Any, Dict, List, Optional
try:
    import pandas
except ImportError:
    pandas = None
from .phase144_models import ResidualDriftBaseline, DriftBaselineSpec
import uuid
import datetime

def create_residual_drift_baseline_id() -> str:
    return f"resid_drift_{uuid.uuid4().hex[:12]}"

def build_residual_drift_baseline(reference_df: Any, monitoring_df: Any, spec: DriftBaselineSpec, prediction_column: str, target_column: str) -> ResidualDriftBaseline:
    return ResidualDriftBaseline(baseline_id=create_residual_drift_baseline_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", spec_id=spec.spec_id, residual_column=f"residual_{prediction_column}", reference_residual_summary={}, monitoring_residual_summary={}, residual_mean_shift=None, residual_std_shift=None, residual_abs_error_shift=None, drift_severity=None, baseline_status=None, research_data_only=True, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, warnings=[], errors=[], risk_flags=[], metadata={})

def compute_residual_summary(df: Any, prediction_column: str, target_column: str) -> Dict[str, Any]:
    return {}

def validate_residual_drift_baseline(item: ResidualDriftBaseline) -> List[str]:
    return []

def residual_drift_summary(item: ResidualDriftBaseline) -> Dict[str, Any]:
    return {}

def residual_drift_to_text(item: ResidualDriftBaseline, limit: int = 300) -> str:
    return "Residual Drift"
