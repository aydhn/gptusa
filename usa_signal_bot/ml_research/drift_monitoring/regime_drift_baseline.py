from typing import Any, Dict, List, Optional
try:
    import pandas
except ImportError:
    pandas = None
from .phase144_models import RegimeDriftBaseline, DriftBaselineSpec
import uuid
import datetime

def create_regime_drift_baseline_id() -> str:
    return f"regime_drift_{uuid.uuid4().hex[:12]}"

def build_regime_drift_baseline(reference_df: Any, monitoring_df: Any, spec: DriftBaselineSpec, regime_column: str = "regime_label") -> RegimeDriftBaseline:
    return RegimeDriftBaseline(baseline_id=create_regime_drift_baseline_id(), created_at_utc=datetime.datetime.utcnow().isoformat() + "Z", spec_id=spec.spec_id, regime_column=regime_column, reference_regime_ratios={}, monitoring_regime_ratios={}, regime_ratio_shift={}, max_regime_shift=None, drift_severity=None, baseline_status=None, research_data_only=True, investment_advice=False, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, warnings=[], errors=[], risk_flags=[], metadata={})

def compute_regime_ratios(df: Any, regime_column: str) -> Dict[str, float]:
    return {}

def compute_regime_ratio_shift(reference_ratios: Dict[str, float], monitoring_ratios: Dict[str, float]) -> Dict[str, float]:
    return {}

def validate_regime_drift_baseline(item: RegimeDriftBaseline) -> List[str]:
    return []

def regime_drift_summary(item: RegimeDriftBaseline) -> Dict[str, Any]:
    return {}

def regime_drift_to_text(item: RegimeDriftBaseline, limit: int = 300) -> str:
    return "Regime Drift"
