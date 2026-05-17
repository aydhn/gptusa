import pytest
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionTradeEvent
from usa_signal_bot.attribution.portfolio_construction_adapter import (
    attach_attribution_to_portfolio_construction_review, portfolio_allocation_status_contribution
)

def _get_mock_review():
    return AttributionReview(
        review_id="r1",
        created_at_utc="now",
        report_type=None,
        events=[AttributionTradeEvent(event_id="e1", symbol="AAPL", sizing_status="APPROVED", net_pnl_usd=100.0)],
        performance_contributions=[],
        risk_contributions=[],
        signal_contributions=[]
    )

def test_attach_attribution_to_portfolio_construction_review():
    payload = {"plan": "A"}
    review = _get_mock_review()
    attached = attach_attribution_to_portfolio_construction_review(payload, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "r1"

def test_portfolio_allocation_status_contribution():
    review = _get_mock_review()
    contribs = portfolio_allocation_status_contribution(review)
    assert len(contribs) == 1
    assert contribs[0].name == "APPROVED"
