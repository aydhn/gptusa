import pytest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from usa_signal_bot.core.enums import AttributionReportType
from usa_signal_bot.attribution.paper_adapter import (
    build_attribution_review_from_paper_payload,
    attach_attribution_to_paper_analytics,
    paper_attribution_summary,
    paper_attribution_warnings
)

@pytest.fixture
def mock_payload() -> Dict[str, Any]:
    return {
        "trades": [
            {"symbol": "AAPL", "net_pnl_usd": 100.0, "total_cost_usd": 1.0},
            {"symbol": "MSFT", "net_pnl_usd": -50.0, "total_cost_usd": 2.0}
        ],
        "other_data": "value"
    }

@patch('usa_signal_bot.attribution.paper_adapter.build_attribution_scorecard')
@patch('usa_signal_bot.attribution.paper_adapter.aggregate_pnl_by_dimension')
@patch('usa_signal_bot.attribution.paper_adapter.normalize_paper_trades')
def test_build_attribution_review_from_paper_payload(mock_normalize, mock_aggregate, mock_scorecard, mock_payload):
    mock_events = [MagicMock(), MagicMock()]
    mock_normalize.return_value = mock_events
    mock_perf_contribs = [MagicMock()]
    mock_aggregate.return_value = mock_perf_contribs
    mock_scorecard_obj = MagicMock()
    mock_scorecard.return_value = mock_scorecard_obj

    result = build_attribution_review_from_paper_payload(mock_payload)

    mock_normalize.assert_called_once_with(mock_payload)
    mock_aggregate.assert_called_once()
    mock_scorecard.assert_called_once_with(mock_events, performance_contributions=mock_perf_contribs)

    assert result.report_type == AttributionReportType.FULL_ATTRIBUTION_REVIEW
    assert result.events == mock_events
    assert result.performance_contributions == mock_perf_contribs
    assert result.scorecard == mock_scorecard_obj
    assert result.warnings == ["Local paper attribution - not real brokerage performance"]
    assert result.review_id.startswith("paper_review")
    assert result.created_at_utc is not None

@patch('usa_signal_bot.attribution.paper_adapter.build_attribution_review_from_paper_payload')
def test_attach_attribution_to_paper_analytics_no_review(mock_build, mock_payload):
    mock_review = MagicMock()
    mock_review.review_id = "test_review_id"
    mock_review.warnings = ["Test warning"]
    mock_build.return_value = mock_review

    result = attach_attribution_to_paper_analytics(mock_payload.copy())

    mock_build.assert_called_once()
    assert "attribution_metadata" in result
    assert result["attribution_metadata"]["review_id"] == "test_review_id"
    assert result["attribution_metadata"]["warnings"] == ["Test warning"]
    assert result["other_data"] == "value"

def test_attach_attribution_to_paper_analytics_with_review(mock_payload):
    review = MagicMock()
    review.review_id = "existing_review_id"
    review.warnings = ["Existing warning"]

    result = attach_attribution_to_paper_analytics(mock_payload.copy(), review=review)

    assert "attribution_metadata" in result
    assert result["attribution_metadata"]["review_id"] == "existing_review_id"
    assert result["attribution_metadata"]["warnings"] == ["Existing warning"]

def test_paper_attribution_summary_exists():
    payload = {
        "attribution_metadata": {
            "review_id": "test_id",
            "warnings": ["warning1"]
        }
    }
    result = paper_attribution_summary(payload)
    assert result == {"review_id": "test_id", "warnings": ["warning1"]}

def test_paper_attribution_summary_missing():
    payload = {"other_data": "value"}
    result = paper_attribution_summary(payload)
    assert result == {}

def test_paper_attribution_warnings_exists():
    payload = {
        "attribution_metadata": {
            "warnings": ["warning1", "warning2"]
        }
    }
    result = paper_attribution_warnings(payload)
    assert result == ["warning1", "warning2"]

def test_paper_attribution_warnings_missing_metadata():
    payload = {"other_data": "value"}
    result = paper_attribution_warnings(payload)
    assert result == []

def test_paper_attribution_warnings_missing_warnings_key():
    payload = {
        "attribution_metadata": {
            "review_id": "test_id"
        }
    }
    result = paper_attribution_warnings(payload)
    assert result == []
