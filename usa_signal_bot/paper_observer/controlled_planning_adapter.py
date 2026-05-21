from typing import Any, Dict, Optional
from usa_signal_bot.paper_observer.observer_models import (
    PaperObserverEnrollment,
    ObserverRuntimeSession,
    PaperObserverReview
)
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment_from_controlled_planning
from usa_signal_bot.paper_observer.observer_runtime_context import build_observer_runtime_context
from usa_signal_bot.paper_observer.parallel_monitor import run_read_only_parallel_monitor
from usa_signal_bot.paper_observer.observer_report import build_paper_observer_review

def observer_enrollment_from_controlled_planning_review(payload: Dict[str, Any]) -> PaperObserverEnrollment:
    return build_observer_enrollment_from_controlled_planning(payload)

def observer_runtime_session_from_controlled_planning_review(
    payload: Dict[str, Any],
    paper_snapshot: Optional[Dict[str, Any]] = None
) -> ObserverRuntimeSession:
    enrollment = observer_enrollment_from_controlled_planning_review(payload)
    context = build_observer_runtime_context(enrollment, paper_snapshot)
    return run_read_only_parallel_monitor(context)

def observer_review_from_controlled_planning_review(
    payload: Dict[str, Any],
    paper_snapshot: Optional[Dict[str, Any]] = None
) -> PaperObserverReview:
    enrollment = observer_enrollment_from_controlled_planning_review(payload)
    context = build_observer_runtime_context(enrollment, paper_snapshot)
    session = run_read_only_parallel_monitor(context)
    return build_paper_observer_review(enrollment, session)

def attach_observer_metadata_to_controlled_planning_payload(payload: Dict[str, Any], review: PaperObserverReview) -> Dict[str, Any]:
    payload["paper_observer_metadata"] = {
        "review_id": review.review_id,
        "enrollments_count": len(review.enrollments),
        "sessions_count": len(review.sessions),
        "drift_events_count": len(review.drift_events)
    }
    return payload

def controlled_planning_observer_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("paper_observer_metadata", {})

def controlled_planning_adapter_to_text(payload: Dict[str, Any]) -> str:
    meta = payload.get("paper_observer_metadata", {})
    return f"Adapter attached observer metadata. Review ID: {meta.get('review_id')}"
