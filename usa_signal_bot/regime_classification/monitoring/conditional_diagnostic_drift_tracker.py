from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftObservation
)
from usa_signal_bot.regime_classification.monitoring.drift_tracking_engine import build_drift_observation
from usa_signal_bot.regime_classification.monitoring.drift_metric_specs import drift_metric_spec_by_name

def track_conditional_diagnostic_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> List[RegimeDriftObservation]:
    obs = []
    spec1 = drift_metric_spec_by_name("warning_diagnostic_count")
    spec2 = drift_metric_spec_by_name("blocking_diagnostic_count")
    if spec1: obs.append(build_drift_observation(baseline, snapshot, spec1))
    if spec2: obs.append(build_drift_observation(baseline, snapshot, spec2))
    return obs

def conditional_warning_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {"baseline_warn": baseline.warning_diagnostic_count, "snapshot_warn": snapshot.warning_diagnostic_count}

def conditional_blocking_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {"baseline_block": baseline.blocking_diagnostic_count, "snapshot_block": snapshot.blocking_diagnostic_count}

def validate_conditional_diagnostic_drift_observations(items: List[RegimeDriftObservation]) -> List[str]:
    return []

def conditional_diagnostic_drift_summary(items: List[RegimeDriftObservation]) -> Dict[str, Any]:
    return {"count": len(items)}
