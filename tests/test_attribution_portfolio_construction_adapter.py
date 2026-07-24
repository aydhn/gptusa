import pytest
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionTradeEvent, AttributionScorecard
from usa_signal_bot.attribution.portfolio_construction_adapter import (
    attach_attribution_to_portfolio_construction_review, portfolio_allocation_status_contribution,
    portfolio_construction_contribution_summary, portfolio_construction_attribution_to_text
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
    # Happy path: valid payload and review
    payload = {"plan": "A"}
    review = _get_mock_review()
    attached = attach_attribution_to_portfolio_construction_review(payload, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "r1"
    assert attached["plan"] == "A"

    # Edge case: Empty payload
    empty_payload = {}
    attached_empty = attach_attribution_to_portfolio_construction_review(empty_payload, review)
    assert "attribution_metadata" in attached_empty
    assert attached_empty["attribution_metadata"]["review_id"] == "r1"

    # Edge case: Review without ID
    class ReviewWithoutID:
        review_id = None

    attached_none_id = attach_attribution_to_portfolio_construction_review({}, ReviewWithoutID())
    assert "attribution_metadata" in attached_none_id
    assert attached_none_id["attribution_metadata"]["review_id"] is None

def test_portfolio_allocation_status_contribution():
    review = _get_mock_review()
    contribs = portfolio_allocation_status_contribution(review)
    assert len(contribs) == 1
    assert contribs[0].name == "APPROVED"

def test_portfolio_construction_contribution_summary():
    review = _get_mock_review()

    # Test without scorecard
    summary1 = portfolio_construction_contribution_summary(review)
    assert summary1 == {"total_trade_count": 0}

    # Test with scorecard
    # Use dummy values for non-default attributes that we don't care about, just to make object creation happy if needed.
    # We will use MagicMock or just a partial AttributionScorecard if it allows, but since it's a dataclass, we must provide required args.
    class MockQuality:
        pass

    scorecard = AttributionScorecard(
        scorecard_id="s1",
        created_at_utc="now",
        total_gross_pnl_usd=0.0,
        total_net_pnl_usd=0.0,
        total_cost_usd=0.0,
        total_trade_count=42,
        positive_contributor_count=0,
        negative_contributor_count=0,
        detrimental_signal_count=0,
        high_risk_contributor_count=0,
        attribution_quality=MockQuality()
    )
    review.scorecard = scorecard

    summary2 = portfolio_construction_contribution_summary(review)
    assert summary2 == {"total_trade_count": 42}

def test_portfolio_construction_attribution_to_text():
    # Test with full payload
    payload = {"attribution_metadata": {"review_id": "r123"}}
    text = portfolio_construction_attribution_to_text(payload)
    assert text == "Portfolio Construction Attribution attached: Review ID r123"

    # Test with missing metadata
    payload_empty = {}
    text_empty = portfolio_construction_attribution_to_text(payload_empty)
    assert text_empty == "Portfolio Construction Attribution attached: Review ID N/A"
