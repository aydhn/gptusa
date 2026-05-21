from typing import Any, Dict
from usa_signal_bot.paper_observer.observer_models import (
    LockedObserverPolicy, PaperObserverEnrollment, ObserverRuntimeContext,
    ObserverOutput, ObserverDriftEvent, ObserverRuntimeSession, ObserverAuditEntry,
    PaperObserverReview
)
from usa_signal_bot.paper_observer.observer_report import paper_observer_limitations_text

def locked_observer_policy_to_text(item: LockedObserverPolicy) -> str:
    return f"LockedObserverPolicy {item.policy_id}"

def observer_enrollment_to_text(item: PaperObserverEnrollment) -> str:
    return f"Enrollment {item.enrollment_id} - {item.status.value}"

def observer_runtime_context_to_text(item: ObserverRuntimeContext) -> str:
    return f"Context {item.context_id} - locked: {item.locked}"

def observer_output_to_text(item: ObserverOutput) -> str:
    return f"Output {item.output_id} - {item.output_type.value}"

def observer_drift_event_to_text(item: ObserverDriftEvent) -> str:
    return f"Drift {item.drift_id} - {item.drift_type.value}"

def observer_runtime_session_to_text(item: ObserverRuntimeSession, limit: int = 100) -> str:
    return f"Session {item.session_id} - {item.status.value}"

def observer_audit_entry_to_text(item: ObserverAuditEntry) -> str:
    return f"Audit {item.audit_id} - {item.action}"

def paper_observer_review_to_text(item: PaperObserverReview, limit: int = 100) -> str:
    return f"Review {item.review_id} - {len(item.sessions)} sessions"

def paper_observer_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
