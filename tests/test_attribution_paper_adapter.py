import pytest
from unittest.mock import patch, MagicMock
from usa_signal_bot.attribution.paper_adapter import (
    build_attribution_review_from_paper_payload,
    attach_attribution_to_paper_analytics,
)
from usa_signal_bot.core.enums import AttributionReportType, AttributionDimension


def _get_mock_payload():
    return {
        "closed_trades": [
            {"symbol": "AAPL", "net_pnl_usd": 100.0, "total_cost_usd": 10.0}
        ]
    }


def test_build_attribution_review_from_paper_payload_integration():
    payload = _get_mock_payload()
    review = build_attribution_review_from_paper_payload(payload)
    assert len(review.events) == 1
    assert review.events[0].symbol == "AAPL"
    assert review.report_type == AttributionReportType.FULL_ATTRIBUTION_REVIEW
    assert any("not real brokerage" in w for w in review.warnings)


@patch("usa_signal_bot.attribution.paper_adapter.build_attribution_scorecard")
@patch("usa_signal_bot.attribution.paper_adapter.aggregate_pnl_by_dimension")
@patch("usa_signal_bot.attribution.paper_adapter.normalize_paper_trades")
def test_build_attribution_review_from_paper_payload_isolated(
    mock_normalize, mock_aggregate, mock_scorecard
):
    mock_events = [MagicMock()]
    mock_contribs = [MagicMock()]
    mock_scorecard_obj = MagicMock()

    mock_normalize.return_value = mock_events
    mock_aggregate.return_value = mock_contribs
    mock_scorecard.return_value = mock_scorecard_obj

    payload = _get_mock_payload()

    review = build_attribution_review_from_paper_payload(payload)

    mock_normalize.assert_called_once_with(payload)
    mock_aggregate.assert_called_once_with(mock_events, AttributionDimension.SYMBOL)
    mock_scorecard.assert_called_once_with(
        mock_events, performance_contributions=mock_contribs
    )

    assert review.events == mock_events
    assert review.performance_contributions == mock_contribs
    assert review.scorecard == mock_scorecard_obj
    assert review.report_type == AttributionReportType.FULL_ATTRIBUTION_REVIEW
    assert review.risk_contributions == []
    assert review.signal_contributions == []
    assert "paper_review_" in review.review_id


def test_build_attribution_review_from_paper_payload_empty():
    payload = {}
    review = build_attribution_review_from_paper_payload(payload)

    assert len(review.events) == 0
    assert review.performance_contributions == []
    assert review.report_type == AttributionReportType.FULL_ATTRIBUTION_REVIEW


def test_attach_attribution_to_paper_analytics():
    payload = _get_mock_payload()
    attached = attach_attribution_to_paper_analytics(payload)
    assert "attribution_metadata" in attached
    assert "review_id" in attached["attribution_metadata"]
