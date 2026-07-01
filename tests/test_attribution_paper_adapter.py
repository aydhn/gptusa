import pytest
from usa_signal_bot.attribution.paper_adapter import (
    build_attribution_review_from_paper_payload,
    attach_attribution_to_paper_analytics,
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


from unittest.mock import MagicMock
from usa_signal_bot.attribution.paper_adapter import (
    paper_attribution_summary,
    paper_attribution_warnings,
)


def test_attach_attribution_to_paper_analytics_with_review():
    payload = {"base": "data"}
    mock_review = MagicMock()
    mock_review.review_id = "test_review_123"
    mock_review.warnings = ["Test warning 1", "Test warning 2"]

    attached = attach_attribution_to_paper_analytics(payload, review=mock_review)

    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "test_review_123"
    assert attached["attribution_metadata"]["warnings"] == [
        "Test warning 1",
        "Test warning 2",
    ]
    assert attached["base"] == "data"


def test_paper_attribution_summary():
    payload = {"attribution_metadata": {"key": "value"}}
    assert paper_attribution_summary(payload) == {"key": "value"}

    empty_payload = {}
    assert paper_attribution_summary(empty_payload) == {}


def test_paper_attribution_warnings():
    payload = {"attribution_metadata": {"warnings": ["w1", "w2"]}}
    assert paper_attribution_warnings(payload) == ["w1", "w2"]

    no_warnings_payload = {"attribution_metadata": {}}
    assert paper_attribution_warnings(no_warnings_payload) == []

    empty_payload = {}
    assert paper_attribution_warnings(empty_payload) == []
