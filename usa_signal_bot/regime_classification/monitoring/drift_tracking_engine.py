import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftMetricSpec,
    RegimeDriftObservation,
    RegimeDriftTrackingResult,
    RegimeDriftMetricKind,
    RegimeDriftDirection,
    RegimeDriftSeverity,
    RegimeMonitoringQuality,
    create_regime_drift_observation_id,
    create_regime_drift_tracking_result_id
)
from usa_signal_bot.regime_classification.monitoring.drift_metric_specs import build_default_drift_metric_specs

def compute_absolute_change(baseline_value: Any, snapshot_value: Any) -> Optional[float]:
    if isinstance(baseline_value, (int, float)) and isinstance(snapshot_value, (int, float)):
        return float(snapshot_value) - float(baseline_value)
    return None

def compute_relative_change(baseline_value: Any, snapshot_value: Any) -> Optional[float]:
    if isinstance(baseline_value, (int, float)) and isinstance(snapshot_value, (int, float)):
        if baseline_value == 0:
            return 0.0 if snapshot_value == 0 else float('inf')
        return (float(snapshot_value) - float(baseline_value)) / abs(float(baseline_value)) * 100.0
    return None

def infer_drift_direction(change: Optional[float], higher_is_worse: bool) -> RegimeDriftDirection:
    if change is None:
        return RegimeDriftDirection.INSUFFICIENT_DATA
    if change == 0:
        return RegimeDriftDirection.STABLE
    if change > 0:
        return RegimeDriftDirection.DEGRADED if higher_is_worse else RegimeDriftDirection.IMPROVED
    return RegimeDriftDirection.IMPROVED if higher_is_worse else RegimeDriftDirection.DEGRADED

def infer_drift_severity(change: Optional[float], spec: RegimeDriftMetricSpec) -> RegimeDriftSeverity:
    if change is None:
        return RegimeDriftSeverity.INSUFFICIENT_DATA
    if spec.metric_kind == RegimeDriftMetricKind.ACCEPTANCE_GATE_STATUS_DRIFT:
        return RegimeDriftSeverity.BLOCKING if change != 0 else RegimeDriftSeverity.NONE

    abs_pct = abs(change) if change != float('inf') else float('inf')
    if abs_pct >= spec.blocking_threshold and spec.blocking_threshold > 0:
        return RegimeDriftSeverity.BLOCKING
    if abs_pct >= spec.warning_threshold and spec.warning_threshold > 0:
        return RegimeDriftSeverity.HIGH
    return RegimeDriftSeverity.NONE

def build_drift_observation(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot, spec: RegimeDriftMetricSpec) -> RegimeDriftObservation:
    b_val = getattr(baseline, spec.baseline_field, None)
    s_val = getattr(snapshot, spec.snapshot_field, None)

    if spec.metric_kind == RegimeDriftMetricKind.ACCEPTANCE_GATE_STATUS_DRIFT:
        rel_change = 1.0 if b_val != s_val else 0.0
        abs_change = rel_change
    else:
        abs_change = compute_absolute_change(b_val, s_val)
        rel_change = compute_relative_change(b_val, s_val)

    direction = infer_drift_direction(rel_change, spec.higher_is_worse) if b_val == s_val else infer_drift_direction(rel_change, spec.higher_is_worse)
    if b_val != s_val and spec.metric_kind == RegimeDriftMetricKind.ACCEPTANCE_GATE_STATUS_DRIFT:
         direction = RegimeDriftDirection.DEGRADED if s_val == "FAILED" else RegimeDriftDirection.IMPROVED
         if s_val == "FAILED":
             severity = RegimeDriftSeverity.BLOCKING
         else:
             severity = RegimeDriftSeverity.NONE
    else:
         severity = infer_drift_severity(rel_change, spec)

    return RegimeDriftObservation(
        observation_id=create_regime_drift_observation_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        metric_name=spec.metric_name,
        metric_kind=spec.metric_kind,
        baseline_value=b_val,
        snapshot_value=s_val,
        absolute_change=abs_change,
        relative_change=rel_change,
        drift_direction=direction,
        drift_severity=severity,
        threshold_used=spec.blocking_threshold if severity == RegimeDriftSeverity.BLOCKING else spec.warning_threshold,
        diagnostic_notes=[],
        research_metadata_only=True,
        investment_advice=False,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def infer_overall_drift_direction(observations: List[RegimeDriftObservation]) -> RegimeDriftDirection:
    has_degraded = any(o.drift_direction == RegimeDriftDirection.DEGRADED for o in observations)
    has_improved = any(o.drift_direction == RegimeDriftDirection.IMPROVED for o in observations)
    if has_degraded and has_improved:
        return RegimeDriftDirection.MIXED
    if has_degraded:
        return RegimeDriftDirection.DEGRADED
    if has_improved:
        return RegimeDriftDirection.IMPROVED
    return RegimeDriftDirection.STABLE

def infer_overall_drift_severity(observations: List[RegimeDriftObservation]) -> RegimeDriftSeverity:
    if any(o.drift_severity == RegimeDriftSeverity.BLOCKING for o in observations):
        return RegimeDriftSeverity.BLOCKING
    if any(o.drift_severity == RegimeDriftSeverity.HIGH for o in observations):
        return RegimeDriftSeverity.HIGH
    return RegimeDriftSeverity.NONE

def track_regime_drift(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot, specs: Optional[List[RegimeDriftMetricSpec]] = None) -> RegimeDriftTrackingResult:
    specs = specs or build_default_drift_metric_specs()
    obs = []
    for spec in specs:
        if hasattr(baseline, spec.baseline_field) and hasattr(snapshot, spec.snapshot_field):
            obs.append(build_drift_observation(baseline, snapshot, spec))

    dir = infer_overall_drift_direction(obs)
    sev = infer_overall_drift_severity(obs)

    return RegimeDriftTrackingResult(
        drift_result_id=create_regime_drift_tracking_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        baseline_id=baseline.baseline_id,
        snapshot_id=snapshot.snapshot_id,
        observations=obs,
        observation_count=len(obs),
        high_drift_count=sum(1 for o in obs if o.drift_severity == RegimeDriftSeverity.HIGH),
        blocking_drift_count=sum(1 for o in obs if o.drift_severity == RegimeDriftSeverity.BLOCKING),
        degraded_count=sum(1 for o in obs if o.drift_direction == RegimeDriftDirection.DEGRADED),
        improved_count=sum(1 for o in obs if o.drift_direction == RegimeDriftDirection.IMPROVED),
        stable_count=sum(1 for o in obs if o.drift_direction == RegimeDriftDirection.STABLE),
        overall_drift_direction=dir,
        overall_drift_severity=sev,
        drift_valid=True,
        quality=RegimeMonitoringQuality.HIGH if sev == RegimeDriftSeverity.NONE else RegimeMonitoringQuality.WARNING,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_drift_tracking_result(result: RegimeDriftTrackingResult) -> List[str]:
    errors = []
    if not result.drift_valid:
        errors.append("Drift result marked as invalid")
    if not result.research_metadata_only:
        errors.append("Drift result is not marked research_metadata_only")
    return errors

def drift_tracking_summary(result: RegimeDriftTrackingResult) -> Dict[str, Any]:
    return {
        "observation_count": result.observation_count,
        "direction": result.overall_drift_direction.value,
        "severity": result.overall_drift_severity.value,
        "blocking_count": result.blocking_drift_count
    }

def drift_tracking_to_text(result: RegimeDriftTrackingResult, limit: int = 300) -> str:
    summ = drift_tracking_summary(result)
    text = f"Drift Tracking: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
