"""Adapter for risk report attribution."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import AttributionReview

def attribution_risk_summary(review: AttributionReview) -> Dict[str, Any]:
    return {
        "high_risk_contributors": len(review.risk_contributions)
    }

def attribution_risk_warnings(review: AttributionReview) -> List[str]:
    warnings = []
    if review.scorecard and review.scorecard.high_risk_contributor_count > 0:
        warnings.append(f"Found {review.scorecard.high_risk_contributor_count} high risk contributors.")
    return warnings

def attach_attribution_to_risk_report(report: Dict[str, Any], review: AttributionReview) -> Dict[str, Any]:
    report["attribution_metadata"] = {
        "review_id": review.review_id,
        "risk_summary": attribution_risk_summary(review),
        "warnings": attribution_risk_warnings(review)
    }
    return report

def attribution_risk_adapter_to_text(payload: Dict[str, Any]) -> str:
    meta = payload.get("attribution_metadata", {})
    return f"Risk Attribution attached: Review ID {meta.get('review_id', 'N/A')}"
