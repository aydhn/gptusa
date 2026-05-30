from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftObservation
)
from usa_signal_bot.regime_classification.monitoring.drift_tracking_engine import build_drift_observation
from usa_signal_bot.regime_classification.monitoring.drift_metric_specs import drift_metric_spec_by_name

def track_acceptance_gate_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> List[RegimeDriftObservation]:
    spec = drift_metric_spec_by_name("acceptance_gate_status")
    if spec:
        return [build_drift_observation(baseline, snapshot, spec)]
    return []

def acceptance_gate_status_changed(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> bool:
    return baseline.acceptance_gate_status != snapshot.acceptance_gate_status

def acceptance_gate_status_drift_summary(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {
        "changed": acceptance_gate_status_changed(baseline, snapshot),
        "baseline_status": baseline.acceptance_gate_status,
        "snapshot_status": snapshot.acceptance_gate_status
    }

def validate_acceptance_gate_drift_observations(items: List[RegimeDriftObservation]) -> List[str]:
    return []

def acceptance_gate_drift_to_text(items: List[RegimeDriftObservation], limit: int = 200) -> str:
    text = f"Acceptance Gate Drift: {len(items)} observations"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
