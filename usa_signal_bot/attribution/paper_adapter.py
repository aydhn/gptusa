"""Adapter for integrating attribution with paper trading results."""

from typing import Any, Dict, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import AttributionReportType
from usa_signal_bot.attribution.attribution_models import AttributionReview, create_attribution_review_id
from usa_signal_bot.attribution.trade_normalizer import normalize_paper_trades
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_scorecard import build_attribution_scorecard

def build_attribution_review_from_paper_payload(payload: Dict[str, Any]) -> AttributionReview:
    events = normalize_paper_trades(payload)
    perf_contribs = aggregate_pnl_by_dimension(events, AttributionDimension.SYMBOL)
    scorecard = build_attribution_scorecard(events, performance_contributions=perf_contribs)

    return AttributionReview(
        review_id=create_attribution_review_id("paper_review"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=AttributionReportType.FULL_ATTRIBUTION_REVIEW,
        events=events,
        performance_contributions=perf_contribs,
        risk_contributions=[],
        signal_contributions=[],
        scorecard=scorecard,
        warnings=["Local paper attribution - not real brokerage performance"]
    )

def attach_attribution_to_paper_analytics(payload: Dict[str, Any], review: AttributionReview = None) -> Dict[str, Any]:
    if not review:
        review = build_attribution_review_from_paper_payload(payload)

    payload["attribution_metadata"] = {
        "review_id": review.review_id,
        "warnings": review.warnings
    }
    return payload

def paper_attribution_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("attribution_metadata", {})

def paper_attribution_warnings(payload: Dict[str, Any]) -> List[str]:
    meta = payload.get("attribution_metadata", {})
    return meta.get("warnings", [])
