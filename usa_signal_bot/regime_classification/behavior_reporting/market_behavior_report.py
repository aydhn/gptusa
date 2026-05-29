from typing import Any
from pathlib import Path

from usa_signal_bot.core.enums import MarketBehaviorReportType, MarketBehaviorStatus
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorContext, MarketBehaviorFullReview
)

def build_market_behavior_context() -> MarketBehaviorContext:
    ctx = MarketBehaviorContext()
    ctx.status = MarketBehaviorStatus.CREATED
    return ctx

def build_market_behavior_full_review() -> MarketBehaviorFullReview:
    rev = MarketBehaviorFullReview()
    rev.report_type = MarketBehaviorReportType.FULL_PHASE130_REVIEW
    return rev

def market_behavior_full_review_summary(review: MarketBehaviorFullReview) -> dict[str, Any]:
    return {"review_id": review.review_id}

def market_behavior_limitations_text() -> str:
    return "Phase 130 limitations apply. This is a local reporting tool only."

def market_behavior_full_review_to_text(review: MarketBehaviorFullReview, limit: int = 300) -> str:
    return f"Full Review: {review.review_id}"
