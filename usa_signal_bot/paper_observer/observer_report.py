from datetime import datetime, timezone
from typing import Any, Dict, Optional
from usa_signal_bot.core.enums import ObserverReportType
from usa_signal_bot.paper_observer.observer_models import (
    PaperObserverReview,
    PaperObserverEnrollment,
    ObserverRuntimeSession,
    create_paper_observer_review_id
)
from usa_signal_bot.paper_observer.observer_audit import audit_entry_from_observer_enrollment, audit_entry_from_observer_session

def build_paper_observer_review(
    enrollment: PaperObserverEnrollment,
    session: Optional[ObserverRuntimeSession] = None
) -> PaperObserverReview:

    audits = [audit_entry_from_observer_enrollment(enrollment)]
    drifts = []

    if session:
        audits.append(audit_entry_from_observer_session(session))
        drifts = session.drift_events

    return PaperObserverReview(
        review_id=create_paper_observer_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=ObserverReportType.FULL_OBSERVER_REVIEW,
        enrollments=[enrollment],
        sessions=[session] if session else [],
        drift_events=drifts,
        audit_entries=audits,
        output_paths={},
        warnings=[],
        errors=[]
    )

def paper_observer_review_summary(review: PaperObserverReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "enrollments_count": len(review.enrollments),
        "sessions_count": len(review.sessions),
        "audit_count": len(review.audit_entries)
    }

def paper_observer_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- No broker/live/demo order.\n"
        "- No active paper enable.\n"
        "- No real paper mutation.\n"
        "- No Telegram real send.\n"
        "- No production config patch.\n"
        "- Observer proposal is not an order.\n"
        "- Human approval is not deployment approval.\n"
        "- NOT INVESTMENT ADVICE."
    )

def paper_observer_review_to_text(review: PaperObserverReview, limit: int = 100) -> str:
    return f"PaperObserverReview {review.review_id} with {len(review.sessions)} sessions."
