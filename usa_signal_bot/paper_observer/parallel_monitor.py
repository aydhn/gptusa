from datetime import datetime, timezone
from typing import Any, Dict, List
from usa_signal_bot.core.enums import ObserverRuntimeStatus
from usa_signal_bot.paper_observer.observer_models import (
    ObserverRuntimeContext,
    ObserverOutput,
    ObserverRuntimeSession,
    create_observer_runtime_session_id
)
from usa_signal_bot.paper_observer.signal_mirror import build_observer_signal_outputs
from usa_signal_bot.paper_observer.proposal_generator import build_observer_proposal_outputs
from usa_signal_bot.paper_observer.risk_mirror import build_observer_risk_outputs
from usa_signal_bot.paper_observer.notification_preview import build_observer_notification_preview
from usa_signal_bot.paper_observer.drift_detector import detect_observer_drift

def collect_parallel_monitor_outputs(context: ObserverRuntimeContext) -> List[ObserverOutput]:
    outputs = []
    signals = build_observer_signal_outputs(context)
    outputs.extend(signals)

    proposals = build_observer_proposal_outputs(context)
    outputs.extend(proposals)

    risks = build_observer_risk_outputs(context, proposals)
    outputs.extend(risks)

    if outputs:
        preview = build_observer_notification_preview(context, outputs)
        outputs.append(preview)

    return outputs

def run_read_only_parallel_monitor(context: ObserverRuntimeContext) -> ObserverRuntimeSession:
    started_at = datetime.now(timezone.utc).isoformat()

    outputs = collect_parallel_monitor_outputs(context)
    drifts = detect_observer_drift(context.read_only_paper_snapshot, outputs)

    completed_at = datetime.now(timezone.utc).isoformat()

    return ObserverRuntimeSession(
        session_id=create_observer_runtime_session_id(),
        created_at_utc=started_at,
        status=ObserverRuntimeStatus.COMPLETED,
        context=context,
        outputs=outputs,
        drift_events=drifts,
        safety_flags=[],
        started_at_utc=started_at,
        completed_at_utc=completed_at,
        output_paths={},
        warnings=[],
        errors=[],
        metadata={}
    )

def validate_parallel_monitor_safety(session: ObserverRuntimeSession) -> List[str]:
    errors = []
    if session.context and not session.context.locked:
        errors.append("Session context is not locked")
    for out in session.outputs:
        if out.is_real_order:
            errors.append(f"Output {out.output_id} is real order")
        if out.mutates_paper_state:
            errors.append(f"Output {out.output_id} mutates paper state")
    return errors

def parallel_monitor_summary(session: ObserverRuntimeSession) -> Dict[str, Any]:
    return {
        "session_id": session.session_id,
        "status": session.status.value,
        "outputs_count": len(session.outputs),
        "drifts_count": len(session.drift_events)
    }

def parallel_monitor_to_text(session: ObserverRuntimeSession) -> str:
    return f"Parallel Monitor Session {session.session_id} - {session.status.value}"
