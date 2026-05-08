from typing import Any, List, Optional
import datetime
import traceback

from usa_signal_bot.core.enums import ObservabilityEventType, ObservabilitySeverity
from usa_signal_bot.observability.observability_models import ObservabilityEvent, create_observability_event_id
from usa_signal_bot.observability.local_logger import sanitize_log_payload

def _new_event(t: ObservabilityEventType, s: ObservabilitySeverity, src: str, msg: str, p: dict) -> ObservabilityEvent:
    return ObservabilityEvent(
        event_id=create_observability_event_id(),
        event_type=t,
        severity=s,
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=src,
        message=msg,
        payload=sanitize_log_payload(p)
    )

def observability_event_from_runtime_event(runtime_event: Any) -> ObservabilityEvent:
    # Handle usa_signal_bot.core.events.RuntimeEvent without tight coupling
    # assume it has event_type, status, message, payload, run_id, step_name
    t = ObservabilityEventType.CUSTOM
    try:
        et = runtime_event.event_type.value
        if "STARTED" in et: t = ObservabilityEventType.RUN_STARTED
        elif "COMPLETED" in et: t = ObservabilityEventType.RUN_COMPLETED
        elif "FAILED" in et: t = ObservabilityEventType.RUN_FAILED
    except Exception:
        pass

    sev = ObservabilitySeverity.INFO
    if "FAIL" in getattr(runtime_event, "status", ""):
        sev = ObservabilitySeverity.ERROR

    return ObservabilityEvent(
        event_id=create_observability_event_id(),
        event_type=t,
        severity=sev,
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source="runtime",
        message=getattr(runtime_event, "message", str(runtime_event)),
        run_id=getattr(runtime_event, "run_id", None),
        step_name=getattr(runtime_event, "step_name", None),
        payload=sanitize_log_payload(getattr(runtime_event, "payload", {}))
    )

def observability_events_from_runtime_events(events: List[Any]) -> List[ObservabilityEvent]:
    return [observability_event_from_runtime_event(e) for e in events]

def observability_event_from_pipeline_step_result(result: Any, run_id: Optional[str] = None) -> ObservabilityEvent:
    sev = ObservabilitySeverity.INFO
    t = ObservabilityEventType.STEP_COMPLETED
    if not getattr(result, "success", True):
        sev = ObservabilitySeverity.ERROR
        t = ObservabilityEventType.STEP_FAILED

    return _new_event(
        t, sev, "pipeline_step",
        f"Step {getattr(result, 'step_name', 'unknown')} completed.",
        {"run_id": run_id, "duration": getattr(result, "duration_seconds", None)}
    )

def observability_events_from_scan_result(scan_result: Any) -> List[ObservabilityEvent]:
    return [_new_event(ObservabilityEventType.CUSTOM, ObservabilitySeverity.INFO, "scan", "Scan completed", {"run_id": getattr(scan_result, "run_id", None)})]

def observability_events_from_paper_result(paper_result: Any) -> List[ObservabilityEvent]:
    return [_new_event(ObservabilityEventType.CUSTOM, ObservabilitySeverity.INFO, "paper", "Paper run completed", {"run_id": getattr(paper_result, "run_id", None)})]

def observability_events_from_quality_result(quality_result: Any) -> List[ObservabilityEvent]:
    return [_new_event(ObservabilityEventType.CUSTOM, ObservabilitySeverity.INFO, "quality", "Quality evaluation completed", {"run_id": getattr(quality_result, "run_id", None)})]

def observability_event_from_exception(source: str, exc: Exception, run_id: Optional[str] = None) -> ObservabilityEvent:
    tb = traceback.format_exc()
    lines = tb.split("\n")
    short_tb = "\n".join(lines[-5:]) if len(lines) > 5 else tb
    p = {"exception_type": type(exc).__name__, "traceback_tail": short_tb}
    if run_id: p["run_id"] = run_id

    return _new_event(ObservabilityEventType.ERROR, ObservabilitySeverity.ERROR, source, str(exc), p)
