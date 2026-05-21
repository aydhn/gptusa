from typing import Any, Dict, List
from usa_signal_bot.core.enums import ObserverOutputType
from usa_signal_bot.paper_observer.observer_models import ObserverRuntimeSession

def observer_session_metrics(session: ObserverRuntimeSession) -> Dict[str, Any]:
    outputs = session.outputs
    return {
        "output_count": len(outputs),
        "signal_mirror_count": sum(1 for o in outputs if o.output_type == ObserverOutputType.SIGNAL_MIRROR),
        "proposal_count": sum(1 for o in outputs if o.output_type == ObserverOutputType.PROPOSAL_MIRROR),
        "risk_output_count": sum(1 for o in outputs if o.output_type == ObserverOutputType.RISK_MIRROR),
        "drift_event_count": len(session.drift_events),
        "safety_flag_count": len(session.safety_flags),
        "blocked_output_count": sum(1 for o in outputs if "blocked" in o.status.lower()),
        "notification_preview_count": sum(1 for o in outputs if o.output_type == ObserverOutputType.NOTIFICATION_PREVIEW)
    }

def observer_session_warning_flags(session: ObserverRuntimeSession) -> List[str]:
    warnings = list(session.warnings)
    for o in session.outputs:
        warnings.extend(o.warnings)
    for d in session.drift_events:
        warnings.extend(d.warnings)
    return list(set(warnings))

def observer_session_block_flags(session: ObserverRuntimeSession) -> List[str]:
    blocks = []
    for f in session.safety_flags:
        blocks.append(f.value)
    return list(set(blocks))

def observer_session_success_flags(session: ObserverRuntimeSession) -> List[str]:
    return ["session_completed"] if session.status.value == "COMPLETED" else []

def analyze_observer_runtime_session(session: ObserverRuntimeSession) -> Dict[str, Any]:
    return {
        "session_id": session.session_id,
        "metrics": observer_session_metrics(session),
        "warnings": observer_session_warning_flags(session),
        "blocks": observer_session_block_flags(session),
        "success": observer_session_success_flags(session)
    }

def observer_monitoring_analyzer_to_text(payload: Dict[str, Any]) -> str:
    metrics = payload.get("metrics", {})
    return f"Analyzer found {metrics.get('output_count', 0)} outputs and {metrics.get('drift_event_count', 0)} drift events."
