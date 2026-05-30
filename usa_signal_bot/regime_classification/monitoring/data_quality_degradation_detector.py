from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    ContextDegradationDiagnostic,
    ContextDegradationProfile
)
from usa_signal_bot.regime_classification.monitoring.drift_metric_specs import drift_metric_spec_by_name
from usa_signal_bot.regime_classification.monitoring.drift_tracking_engine import build_drift_observation
from usa_signal_bot.regime_classification.monitoring.context_degradation_detector import build_degradation_diagnostic_from_observation, build_default_context_degradation_rules, ContextDegradationKind

def detect_data_quality_degradation(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> List[ContextDegradationDiagnostic]:
    spec = drift_metric_spec_by_name("data_quality_limited_count")
    if not spec:
        return []
    obs = build_drift_observation(baseline, snapshot, spec)
    rules = build_default_context_degradation_rules()
    rule = next((r for r in rules if r.degradation_kind == ContextDegradationKind.DATA_QUALITY_DEGRADATION), rules[0])

    if obs.drift_severity != "NONE":
         return [build_degradation_diagnostic_from_observation(obs, rule)]
    return []

def data_quality_limited_count_change(baseline: RegimeMonitoringBaseline, snapshot: RegimeMonitoringSnapshot) -> Dict[str, Any]:
    return {"baseline_count": baseline.data_quality_limited_count, "snapshot_count": snapshot.data_quality_limited_count}

def build_data_quality_degradation_profile(items: List[ContextDegradationDiagnostic]) -> ContextDegradationProfile:
    from usa_signal_bot.regime_classification.monitoring.context_degradation_detector import build_context_degradation_profiles
    profiles = build_context_degradation_profiles(items)
    return profiles[0] if profiles else None

def validate_data_quality_degradation(items: List[ContextDegradationDiagnostic]) -> List[str]:
    return []

def data_quality_degradation_summary(items: List[ContextDegradationDiagnostic]) -> Dict[str, Any]:
    return {"count": len(items)}

def data_quality_degradation_to_text(items: List[ContextDegradationDiagnostic], limit: int = 200) -> str:
    text = f"Data Quality Degradation: {len(items)} diagnostics"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
