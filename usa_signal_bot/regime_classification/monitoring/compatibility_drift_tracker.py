from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftObservation,
    RegimeDriftMetricKind
)
from usa_signal_bot.regime_classification.monitoring.drift_tracking_engine import build_drift_observation
from usa_signal_bot.regime_classification.monitoring.drift_metric_specs import drift_metric_spec_by_name

def track_compatibility_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> List[RegimeDriftObservation]:
    obs = []
    spec1 = drift_metric_spec_by_name("compatibility_result_count")
    spec2 = drift_metric_spec_by_name("low_compatibility_count")
    if spec1: obs.append(build_drift_observation(baseline, snapshot, spec1))
    if spec2: obs.append(build_drift_observation(baseline, snapshot, spec2))
    return obs

def compatibility_count_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {"baseline_count": baseline.compatibility_result_count, "snapshot_count": snapshot.compatibility_result_count}

def compatibility_quality_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {"baseline_low_count": baseline.low_compatibility_count, "snapshot_low_count": snapshot.low_compatibility_count}

def validate_compatibility_drift_observations(items: List[RegimeDriftObservation]) -> List[str]:
    return []

def compatibility_drift_summary(items: List[RegimeDriftObservation]) -> Dict[str, Any]:
    return {"count": len(items)}
