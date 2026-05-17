"""Adapter for integrating attribution with backtest results."""

from typing import Any, Dict, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import AttributionReportType
from usa_signal_bot.attribution.attribution_models import AttributionReview, create_attribution_review_id, attribution_review_to_dict
from usa_signal_bot.attribution.trade_normalizer import normalize_backtest_trades
from usa_signal_bot.attribution.pnl_attribution import aggregate_pnl_by_dimension
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.attribution_scorecard import build_attribution_scorecard

def build_attribution_review_from_backtest_result(result: Dict[str, Any]) -> AttributionReview:
    events = normalize_backtest_trades(result)
    perf_contribs = aggregate_pnl_by_dimension(events, AttributionDimension.STRATEGY)

    scorecard = build_attribution_scorecard(events, performance_contributions=perf_contribs)

    return AttributionReview(
        review_id=create_attribution_review_id("bt_review"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=AttributionReportType.PERFORMANCE_ATTRIBUTION,
        events=events,
        performance_contributions=perf_contribs,
        risk_contributions=[],
        signal_contributions=[],
        scorecard=scorecard
    )

def attach_attribution_to_backtest_result(result: Dict[str, Any], review: AttributionReview = None) -> Dict[str, Any]:
    if not review:
        review = build_attribution_review_from_backtest_result(result)

    result["attribution_metadata"] = {
        "review_id": review.review_id,
        "scorecard": review.scorecard.summary_scores if review.scorecard else {},
        "warnings": review.warnings
    }
    return result

def backtest_attribution_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("attribution_metadata", {})

def backtest_attribution_warnings(result: Dict[str, Any]) -> List[str]:
    meta = result.get("attribution_metadata", {})
    return meta.get("warnings", [])
