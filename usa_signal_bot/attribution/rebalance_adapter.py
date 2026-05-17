"""Adapter for rebalance attribution."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import AttributionReview
from usa_signal_bot.attribution.rebalance_attribution import rebalance_pnl_proxy_summary, turnover_cost_attribution

def attach_attribution_to_rebalance_review(review_payload: Dict[str, Any], attribution_review: AttributionReview) -> Dict[str, Any]:
    review_payload["attribution_metadata"] = {
        "review_id": attribution_review.review_id
    }
    return review_payload

def rebalance_action_contribution_summary(attribution_review: AttributionReview) -> Dict[str, Any]:
    return rebalance_pnl_proxy_summary(attribution_review.events)

def rebalance_turnover_contribution_summary(attribution_review: AttributionReview) -> Dict[str, Any]:
    contribs = turnover_cost_attribution(attribution_review.events)
    return {c.name: c.total_cost_usd for c in contribs}

def rebalance_attribution_adapter_to_text(payload: Dict[str, Any]) -> str:
    meta = payload.get("attribution_metadata", {})
    return f"Rebalance Attribution attached: Review ID {meta.get('review_id', 'N/A')}"
