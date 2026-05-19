from typing import Any
from datetime import datetime
from usa_signal_bot.research_governance.governance_models import (
    GovernanceReview, PromotionReview, ReleaseCandidatePackage, GovernanceReportType,
    create_governance_review_id
)

def governance_review_from_research_execution_review(execution_payload: dict[str, Any]) -> GovernanceReview:
    return GovernanceReview(
        governance_review_id=create_governance_review_id(),
        created_at_utc=datetime.utcnow().isoformat(),
        report_type=GovernanceReportType.FULL_GOVERNANCE_REVIEW,
        evidence_packs=[],
        promotion_reviews=[],
        release_candidates=[],
        decision_board_results=[],
        decision_logs=[],
        audit_trails=[],
        output_paths={},
        warnings=[], errors=[]
    )

def promotion_reviews_from_comparison_reports(execution_payload: dict[str, Any]) -> list[PromotionReview]:
    return []

def release_candidates_from_execution_review(execution_payload: dict[str, Any]) -> list[ReleaseCandidatePackage]:
    return []

def attach_governance_to_execution_review(execution_payload: dict[str, Any], governance_review: GovernanceReview) -> dict[str, Any]:
    execution_payload["governance"] = governance_review.governance_review_id
    return execution_payload

def research_execution_governance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def research_execution_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Research Execution Adapter"
