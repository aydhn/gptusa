from typing import Any
from usa_signal_bot.feature_engine.factor_validation.phase122_models import FactorDriftStatus

def compute_mean_shift(baseline: dict[str, Any], observed: dict[str, Any]) -> float:
    b = baseline.get("mean", 0.0)
    o = observed.get("mean", 0.0)
    if b is None or o is None or b == 0: return 0.0
    return abs(o - b) / abs(b)

def compute_std_shift(baseline: dict[str, Any], observed: dict[str, Any]) -> float:
    b = baseline.get("std", 0.0)
    o = observed.get("std", 0.0)
    if b is None or o is None or b == 0: return 0.0
    return abs(o - b) / abs(b)

def compute_median_shift(baseline: dict[str, Any], observed: dict[str, Any]) -> float:
    b = baseline.get("median", 0.0)
    o = observed.get("median", 0.0)
    if b is None or o is None or b == 0: return 0.0
    return abs(o - b) / abs(b)

def compute_null_rate_shift(baseline: dict[str, Any], observed: dict[str, Any]) -> float:
    bc, bn = baseline.get("count", 0), baseline.get("null_count", 0)
    oc, on = observed.get("count", 0), observed.get("null_count", 0)
    if bc == 0 or oc == 0: return 0.0
    return abs((on/oc) - (bn/bc))

def compute_finite_rate_shift(baseline: dict[str, Any], observed: dict[str, Any]) -> float:
    return 0.0

def compute_outlier_rate_shift(baseline: dict[str, Any], observed: dict[str, Any]) -> float:
    return 0.0

def drift_status_from_score(score: float) -> FactorDriftStatus:
    if score < 20: return FactorDriftStatus.NO_DRIFT
    if score < 40: return FactorDriftStatus.LOW_DRIFT
    if score < 70: return FactorDriftStatus.MODERATE_DRIFT
    if score < 90: return FactorDriftStatus.HIGH_DRIFT
    return FactorDriftStatus.CRITICAL_DRIFT

def validate_drift_metric_values(values: list[float]) -> list[str]:
    return []

def factor_drift_metrics_summary(observations: list[Any]) -> dict[str, Any]:
    return {"observations_count": len(observations)}
