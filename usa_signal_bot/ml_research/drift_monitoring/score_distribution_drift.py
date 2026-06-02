from typing import Any, Dict, List, Optional
try:
    import pandas
except ImportError:
    pandas = None
from .phase144_models import ScoreDistributionDriftBaseline, DriftBaselineSpec
import uuid
import datetime

def create_score_distribution_drift_baseline_id() -> str:
    return f"score_drift_{uuid.uuid4().hex[:12]}"

def build_score_distribution_drift_baseline(reference_df: Any, monitoring_df: Any, spec: DriftBaselineSpec, score_column: str = "research_ensemble_prediction_score") -> ScoreDistributionDriftBaseline:
    return ScoreDistributionDriftBaseline(baseline_id=create_score_distribution_drift_baseline_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", spec_id=spec.spec_id, score_column=score_column, reference_quantiles={}, monitoring_quantiles={}, mean_shift=None, median_shift=None, std_shift=None, psi_approx=None, drift_severity=None, baseline_status=None, row_count_reference=0, row_count_monitoring=0, research_data_only=True, investment_advice=False, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, warnings=[], errors=[], risk_flags=[], metadata={})

def compute_score_quantiles(series: Any) -> Dict[str, float]:
    return {}

def calculate_psi_approx(reference_series: Any, monitoring_series: Any, bins: int = 10) -> Optional[float]:
    return None

def validate_score_distribution_drift_baseline(item: ScoreDistributionDriftBaseline) -> List[str]:
    return []

def score_distribution_drift_summary(item: ScoreDistributionDriftBaseline) -> Dict[str, Any]:
    return {}

def score_distribution_drift_to_text(item: ScoreDistributionDriftBaseline, limit: int = 300) -> str:
    return "Score Drift"
