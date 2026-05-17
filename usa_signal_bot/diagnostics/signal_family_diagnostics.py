from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent, FailureCluster
from usa_signal_bot.diagnostics.false_signal_analysis import false_signal_assessments_by_signal_family, identify_false_positive_events
from usa_signal_bot.diagnostics.cost_degradation_analysis import identify_cost_degraded_events

def diagnose_signal_family(signal_family: str, events: List[DiagnosticEvent]) -> Dict[str, Any]:
    family_events = [e for e in events if e.signal_family == signal_family]
    fps = identify_false_positive_events(family_events)
    degraded = identify_cost_degraded_events(family_events)

    return {
        "signal_family": signal_family,
        "event_count": len(family_events),
        "false_positive_count": len(fps),
        "cost_degraded_count": len(degraded)
    }

def diagnose_signal_families(events: List[DiagnosticEvent]) -> List[Dict[str, Any]]:
    families = set(e.signal_family for e in events if e.signal_family)
    return [diagnose_signal_family(f, events) for f in families]

def signal_family_false_positive_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    fps = identify_false_positive_events(events)
    return {"total_false_positives": len(fps)}

def signal_family_cost_degradation_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    degraded = identify_cost_degraded_events(events)
    return {"total_cost_degraded": len(degraded)}

def signal_family_failure_clusters(events: List[DiagnosticEvent]) -> List[FailureCluster]:
    # Could use detect_repeated_loss_patterns, customized for signal family
    from usa_signal_bot.diagnostics.loss_event_analysis import detect_repeated_loss_patterns
    return detect_repeated_loss_patterns(events)

def signal_family_diagnostics_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Signal Family Diagnostics:",
        f"  Total False Positives: {payload.get('total_false_positives', 0)}"
    ]
    return "\n".join(lines)
