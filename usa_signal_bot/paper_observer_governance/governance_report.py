from typing import Any
from .observer_governance_models import ObserverGovernanceReview, create_observer_governance_review_id
from usa_signal_bot.core.enums import ObserverGovernanceReportType
from datetime import datetime, timezone

def build_observer_governance_review(observer_payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None, controlled_planning_payload: dict[str, Any] | None = None, observation_payload: dict[str, Any] | None = None) -> ObserverGovernanceReview:
    return ObserverGovernanceReview(
        review_id=create_observer_governance_review_id(), created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=ObserverGovernanceReportType.FULL_OBSERVER_GOVERNANCE_REVIEW,
        comparison_reports=[], evidence_refreshes=[], gates=[], decisions=[], audit_entries=[],
        output_paths={}, warnings=[], errors=[]
    )

def observer_governance_review_summary(review: ObserverGovernanceReview) -> dict[str, Any]:
    return {"review_id": review.review_id, "decisions": len(review.decisions)}

def observer_governance_limitations_text() -> str:
    return "Observer governance is non-executing. No active paper enable, no paper mutation, no live order, no broker execution, no real Telegram send, no config patch. Not investment advice."

def observer_governance_review_to_text(review: ObserverGovernanceReview, limit: int = 100) -> str:
    return str(observer_governance_review_summary(review)) + " | " + observer_governance_limitations_text()
