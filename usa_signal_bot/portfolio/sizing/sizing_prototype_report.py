from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import (
    SizingPrototypeContext, SizingPrototypeFullReview, SizingPrototypeReportType
)

def build_sizing_prototype_context() -> SizingPrototypeContext:
    return SizingPrototypeContext()

def build_sizing_prototype_full_review() -> SizingPrototypeFullReview:
    return SizingPrototypeFullReview(report_type=SizingPrototypeReportType.FULL_PHASE154_REVIEW)

def sizing_prototype_full_review_summary(review: SizingPrototypeFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase155": review.phase155_readiness_gate.ready_for_phase155
    }

def sizing_prototype_limitations_text() -> str:
    return "Limitations: This is a research prototype only. It does not produce actual position sizes, target weights, allocations, or order sizes. It is not investment advice and performs no live trading."

def sizing_prototype_full_review_to_text(review: SizingPrototypeFullReview, limit: int = 300) -> str:
    return f"Sizing Prototype Full Review: {review.review_id}, Ready Phase 155: {review.phase155_readiness_gate.ready_for_phase155}"[:limit]
