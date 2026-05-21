from typing import Any
from .observer_governance_models import ObserverGovernanceReview, ObserverPaperComparisonReport
from .governance_report import build_observer_governance_review
from .observer_paper_comparator import compare_observer_to_paper

def governance_review_from_paper_observer_review(payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> ObserverGovernanceReview:
    return build_observer_governance_review(payload, paper_snapshot)

def comparison_from_paper_observer_review(payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> ObserverPaperComparisonReport:
    return compare_observer_to_paper(paper_snapshot or {}, payload)

def attach_governance_metadata_to_observer_payload(payload: dict[str, Any], review: ObserverGovernanceReview) -> dict[str, Any]:
    payload["governance_review_id"] = review.review_id
    return payload

def paper_observer_governance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"governance_review_id": payload.get("governance_review_id")}

def paper_observer_adapter_to_text(payload: dict[str, Any]) -> str:
    return str(paper_observer_governance_summary(payload))
