import pytest
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionTradeEvent
from usa_signal_bot.attribution.rebalance_adapter import (
    attach_attribution_to_rebalance_review, rebalance_action_contribution_summary
)

def _get_mock_review():
    return AttributionReview(
        review_id="r1",
        created_at_utc="now",
        report_type=None,
        events=[AttributionTradeEvent(event_id="e1", symbol="AAPL", rebalance_action_type="INCREASE", net_pnl_usd=100.0)],
        performance_contributions=[],
        risk_contributions=[],
        signal_contributions=[]
    )

def test_attach_attribution_to_rebalance_review():
    # Test with empty payload
    payload = {}
    review = _get_mock_review()
    attached = attach_attribution_to_rebalance_review(payload, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "r1"

    # Test with existing payload
    payload = {"status": "ok", "some_key": "some_value"}
    attached = attach_attribution_to_rebalance_review(payload, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "r1"
    assert attached["status"] == "ok"
    assert attached["some_key"] == "some_value"

    # Test with existing attribution_metadata (should be overwritten)
    payload = {"attribution_metadata": {"review_id": "old_id"}}
    attached = attach_attribution_to_rebalance_review(payload, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "r1"


def test_rebalance_action_contribution_summary():
    review = _get_mock_review()
    summary = rebalance_action_contribution_summary(review)
    assert "INCREASE" in summary
    assert summary["INCREASE"] == 100.0
