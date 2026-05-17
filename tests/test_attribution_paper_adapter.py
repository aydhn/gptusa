import pytest
from usa_signal_bot.attribution.paper_adapter import (
    build_attribution_review_from_paper_payload, attach_attribution_to_paper_analytics
)

def _get_mock_payload():
    return {
        "closed_trades": [
            {"symbol": "AAPL", "net_pnl_usd": 100.0, "total_cost_usd": 10.0}
        ]
    }

def test_build_attribution_review_from_paper_payload():
    payload = _get_mock_payload()
    review = build_attribution_review_from_paper_payload(payload)
    assert len(review.events) == 1
    assert review.events[0].symbol == "AAPL"
    assert any("not real brokerage" in w for w in review.warnings)

def test_attach_attribution_to_paper_analytics():
    payload = _get_mock_payload()
    attached = attach_attribution_to_paper_analytics(payload)
    assert "attribution_metadata" in attached
    assert "review_id" in attached["attribution_metadata"]
