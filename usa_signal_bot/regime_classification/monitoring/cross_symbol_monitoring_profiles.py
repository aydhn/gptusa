from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    ContextDegradationDiagnostic,
    ContextDegradationProfile,
    ContextDegradationStatus
)
from usa_signal_bot.regime_classification.monitoring.context_degradation_detector import build_context_degradation_profiles

def build_cross_symbol_monitoring_profile(diagnostics: List[ContextDegradationDiagnostic]) -> ContextDegradationProfile:
    profiles = build_context_degradation_profiles(diagnostics)
    return profiles[0] if profiles else None

def compute_cross_symbol_degradation_distribution(diagnostics: List[ContextDegradationDiagnostic]) -> Dict[str, Any]:
    dist = {}
    for d in diagnostics:
        status_val = d.status.value
        dist[status_val] = dist.get(status_val, 0) + 1
    return dist

def compute_cross_symbol_blocked_count(diagnostics: List[ContextDegradationDiagnostic]) -> int:
    return sum(1 for d in diagnostics if d.status == ContextDegradationStatus.BLOCKED)

def validate_cross_symbol_monitoring_profile(profile: ContextDegradationProfile) -> List[str]:
    return []

def cross_symbol_monitoring_summary(profile: ContextDegradationProfile) -> Dict[str, Any]:
    if not profile: return {}
    return {
        "status": profile.profile_status.value,
        "blocked_count": profile.blocked_count
    }

def cross_symbol_monitoring_to_text(profile: ContextDegradationProfile) -> str:
    if not profile: return "No Cross Symbol Profile"
    return f"Cross Symbol Profile: {profile.profile_status.value}"
