from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
from usa_signal_bot.core.enums import ObserverRuntimeMode, ObserverMonitoringMode
from usa_signal_bot.paper_observer.observer_models import (
    ObserverRuntimeContext,
    PaperObserverEnrollment,
    create_observer_runtime_context_id
)

def build_observer_runtime_context(
    enrollment: PaperObserverEnrollment,
    paper_snapshot: Optional[Dict[str, Any]] = None,
    runtime_mode: ObserverRuntimeMode = ObserverRuntimeMode.FULL_LOCKED_OBSERVER,
    monitoring_mode: ObserverMonitoringMode = ObserverMonitoringMode.FULL_READ_ONLY_PARALLEL_MONITOR
) -> ObserverRuntimeContext:

    snapshot = paper_snapshot if paper_snapshot else {}

    return ObserverRuntimeContext(
        context_id=create_observer_runtime_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        enrollment_id=enrollment.enrollment_id,
        candidate_id=enrollment.candidate_id,
        runtime_mode=runtime_mode,
        monitoring_mode=monitoring_mode,
        read_only_paper_snapshot=snapshot,
        candidate_metadata={},
        output_path=None,
        locked=True,
        allow_active_paper=False,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_config_patch=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def build_mock_observer_runtime_context() -> ObserverRuntimeContext:
    from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment
    mock_enrollment = build_observer_enrollment("mock_cand", "mock_ticket", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    return build_observer_runtime_context(mock_enrollment, {})

def validate_observer_context_safety(context: ObserverRuntimeContext) -> List[str]:
    errors = []
    if not context.locked:
        errors.append("Context must have locked=True")
    if context.allow_active_paper:
        errors.append("Context cannot allow active paper")
    if context.allow_paper_state_mutation:
        errors.append("Context cannot allow paper state mutation")
    if context.allow_paper_orders:
        errors.append("Context cannot allow paper orders")
    if context.allow_broker_orders:
        errors.append("Context cannot allow broker orders")
    if context.allow_telegram_real_send:
        errors.append("Context cannot allow Telegram real send")
    if context.allow_config_patch:
        errors.append("Context cannot allow config patch")
    return errors

def observer_context_summary(context: ObserverRuntimeContext) -> Dict[str, Any]:
    return {
        "context_id": context.context_id,
        "runtime_mode": context.runtime_mode.value,
        "monitoring_mode": context.monitoring_mode.value,
        "locked": context.locked
    }

def observer_context_to_text(context: ObserverRuntimeContext) -> str:
    return f"ObserverRuntimeContext {context.context_id} (Locked: {context.locked})"
