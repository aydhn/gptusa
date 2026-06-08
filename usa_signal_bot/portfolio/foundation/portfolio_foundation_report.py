from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioFoundationContext, PortfolioFoundationFullReview, PortfolioFoundationReportType
)

def build_portfolio_foundation_context() -> PortfolioFoundationContext:
    return PortfolioFoundationContext()

def build_portfolio_foundation_full_review() -> PortfolioFoundationFullReview:
    return PortfolioFoundationFullReview()

def portfolio_foundation_full_review_summary(review: PortfolioFoundationFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase154": review.phase154_readiness_gate.ready_for_phase154,
        "safety_passed": review.safety_boundary.boundary_passed
    }

def portfolio_foundation_limitations_text() -> str:
    return """
Phase 153 Limitations:
- Phase 153 is a contract-only portfolio foundation, position sizing boundary, and risk budgeting contract phase.
- Actual portfolio construction is NOT performed.
- Actual position sizing is NOT performed.
- Target weights, allocation output, and capital deployment are NOT generated.
- No live trading, paper trading, broker execution, or order creation.
- The outputs are strictly research metadata and DO NOT constitute investment advice.
- Phase 154 will introduce deterministic position sizing prototypes and sizing diagnostics.
"""

def portfolio_foundation_full_review_to_text(review: PortfolioFoundationFullReview, limit: int = 300) -> str:
    lines = [
        "Portfolio Foundation Full Review:",
        f"Review ID: {review.review_id}",
        f"Ready for Phase 154: {review.phase154_readiness_gate.ready_for_phase154}",
        f"Safety Passed: {review.safety_boundary.boundary_passed}",
        portfolio_foundation_limitations_text()
    ]
    return "\n".join(lines)
