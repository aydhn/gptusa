import pytest
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionTradeEvent
from usa_signal_bot.attribution.allocation_adapter import attach_attribution_to_allocation_review

def _get_mock_review():
    return AttributionReview(
        review_id="r1",
        created_at_utc="now",
        report_type=None,
        events=[AttributionTradeEvent(event_id="e1", symbol="AAPL", sizing_status="CAPPED", net_pnl_usd=100.0)],
        performance_contributions=[],
        risk_contributions=[],
        signal_contributions=[]
    )

def test_attach_attribution_to_allocation_review():
    payload = {"status": "ok"}
    review = _get_mock_review()
    attached = attach_attribution_to_allocation_review(payload, review)
    assert "attribution_metadata" in attached
