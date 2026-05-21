from typing import Any

def extract_observer_metrics(observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "observer_session_count": len(observer_payload.get("sessions", [])),
        "observer_output_count": len(observer_payload.get("outputs", [])),
        **extract_observer_output_counts(observer_payload),
        **extract_observer_drift_metrics(observer_payload),
        **extract_observer_safety_metrics(observer_payload)
    }

def extract_observer_output_counts(observer_payload: dict[str, Any]) -> dict[str, int]:
    return {
        "signal_mirror_count": observer_payload.get("signal_mirror_count", 0),
        "proposal_count": observer_payload.get("proposal_count", 0),
        "risk_output_count": observer_payload.get("risk_output_count", 0),
        "notification_preview_count": observer_payload.get("notification_preview_count", 0)
    }

def extract_observer_drift_metrics(observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"drift_event_count": len(observer_payload.get("drift_events", []))}

def extract_observer_safety_metrics(observer_payload: dict[str, Any]) -> dict[str, int]:
    return {
        "safety_flag_count": observer_payload.get("safety_flag_count", 0),
        "blocked_output_count": observer_payload.get("blocked_output_count", 0),
        "locked_runtime_count": observer_payload.get("locked_runtime_count", 1)
    }

def required_observer_metrics() -> list[str]:
    return [
        "observer_session_count", "observer_output_count", "signal_mirror_count",
        "proposal_count", "risk_output_count", "notification_preview_count",
        "drift_event_count", "safety_flag_count", "blocked_output_count", "locked_runtime_count"
    ]

def observer_metric_quality_warnings(metrics: dict[str, Any]) -> list[str]:
    warnings = []
    if metrics.get("observer_session_count", 0) == 0: warnings.append("0 observer sessions.")
    if metrics.get("observer_output_count", 0) == 0: warnings.append("0 observer outputs.")
    return warnings

def observer_metric_extractor_to_text(metrics: dict[str, Any]) -> str:
    return str(metrics)
