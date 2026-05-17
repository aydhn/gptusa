"""Adapter for allocation attribution."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionContribution
from usa_signal_bot.attribution.sizing_attribution import sizing_status_attribution

def attach_attribution_to_allocation_review(review_payload: Dict[str, Any], attribution_review: AttributionReview) -> Dict[str, Any]:
    review_payload["attribution_metadata"] = {
        "review_id": attribution_review.review_id
    }
    return review_payload

def allocation_sizing_status_contribution(attribution_review: AttributionReview) -> List[AttributionContribution]:
    return sizing_status_attribution(attribution_review.events)

def allocation_risk_budget_contribution_summary(attribution_review: AttributionReview) -> Dict[str, Any]:
    return {"risk_budget_contribution": "Mocked budget contribution."}

def allocation_attribution_adapter_to_text(payload: Dict[str, Any]) -> str:
    meta = payload.get("attribution_metadata", {})
    return f"Allocation Attribution attached: Review ID {meta.get('review_id', 'N/A')}"
