"""Adapter for portfolio construction attribution."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionContribution
from usa_signal_bot.attribution.sizing_attribution import sizing_status_attribution

def attach_attribution_to_portfolio_construction_review(review_payload: Dict[str, Any], attribution_review: AttributionReview) -> Dict[str, Any]:
    review_payload["attribution_metadata"] = {
        "review_id": attribution_review.review_id
    }
    return review_payload

def portfolio_construction_contribution_summary(attribution_review: AttributionReview) -> Dict[str, Any]:
    return {"total_trade_count": attribution_review.scorecard.total_trade_count if attribution_review.scorecard else 0}

def portfolio_allocation_status_contribution(attribution_review: AttributionReview) -> List[AttributionContribution]:
    return sizing_status_attribution(attribution_review.events)

def portfolio_construction_attribution_to_text(payload: Dict[str, Any]) -> str:
    meta = payload.get("attribution_metadata", {})
    return f"Portfolio Construction Attribution attached: Review ID {meta.get('review_id', 'N/A')}"
