import pytest
from usa_signal_bot.attribution.walk_forward_adapter import (
    build_attribution_by_walk_forward_window, attach_attribution_to_walk_forward_result,
    walk_forward_attribution_summary, walk_forward_attribution_warnings
)
from unittest.mock import MagicMock

def _get_mock_result():
    return {
        "windows": [
            {"trades": [{"symbol": "AAPL", "net_pnl_usd": 100.0, "strategy_name": "Trend"}]},
            {"trades": [{"symbol": "MSFT", "net_pnl_usd": -50.0, "strategy_name": "MeanRev"}]}
        ]
    }

def test_build_attribution_by_walk_forward_window():
    result = _get_mock_result()
    reviews = build_attribution_by_walk_forward_window(result)
    assert len(reviews) == 2
    assert "window_0" in reviews
    assert "window_1" in reviews

def test_attach_attribution_to_walk_forward_result():
    result = _get_mock_result()
    attached = attach_attribution_to_walk_forward_result(result)
    assert "attribution_metadata" in attached
    assert "window_reviews" in attached["attribution_metadata"]
    assert "warnings" in attached
    assert any("negative contributor" in w for w in attached["warnings"])

def test_build_attribution_by_walk_forward_window_happy_path():
    result = {"windows": [{"trades": []}]}
    reviews = build_attribution_by_walk_forward_window(result)
    assert len(reviews) == 1
    assert "window_0" in reviews

def test_build_attribution_by_walk_forward_window_edge_cases():
    result = {}
    reviews = build_attribution_by_walk_forward_window(result)
    assert len(reviews) == 0

    result = {"windows": []}
    reviews = build_attribution_by_walk_forward_window(result)
    assert len(reviews) == 0



def test_attach_attribution_to_walk_forward_result_explicit_reviews():
    mock_review_1 = MagicMock()
    mock_review_1.review_id = "test_review_1"
    mock_review_1.scorecard = None

    result = {}
    reviews = {"window_0": mock_review_1}

    attached = attach_attribution_to_walk_forward_result(result, reviews)

    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["window_reviews"] == {"window_0": "test_review_1"}
    assert "warnings" not in attached

def test_attach_attribution_to_walk_forward_result_missing_scorecard():
    mock_review_1 = MagicMock()
    mock_review_1.review_id = "test_review_1"
    mock_review_1.scorecard = None

    result = {}
    reviews = {"window_0": mock_review_1}

    attached = attach_attribution_to_walk_forward_result(result, reviews)

    assert "attribution_metadata" in attached
    assert "warnings" not in attached

def test_attach_attribution_to_walk_forward_result_positive_pnl():
    mock_review_1 = MagicMock()
    mock_review_1.review_id = "test_review_1"
    mock_review_1.scorecard.total_net_pnl_usd = 100.0

    result = {}
    reviews = {"window_0": mock_review_1}

    attached = attach_attribution_to_walk_forward_result(result, reviews)

    assert "attribution_metadata" in attached
    assert "warnings" not in attached

def test_attach_attribution_to_walk_forward_result_existing_warnings():
    mock_review_1 = MagicMock()
    mock_review_1.review_id = "test_review_1"
    mock_review_1.scorecard.total_net_pnl_usd = -50.0

    result = {"warnings": ["Existing warning"]}
    reviews = {"window_0": mock_review_1}

    attached = attach_attribution_to_walk_forward_result(result, reviews)

    assert "attribution_metadata" in attached
    assert "warnings" in attached
    assert len(attached["warnings"]) == 2
    assert attached["warnings"][0] == "Existing warning"
    assert attached["warnings"][1] == "OOS window window_0 has negative contributor"

def test_walk_forward_attribution_summary():
    assert walk_forward_attribution_summary({}) == {}
    assert walk_forward_attribution_summary({"attribution_metadata": {"a": 1}}) == {"a": 1}

def test_walk_forward_attribution_warnings():
    assert walk_forward_attribution_warnings({}) == []
    assert walk_forward_attribution_warnings({"warnings": ["w1", "w2"]}) == ["w1", "w2"]

def test_attach_attribution_to_walk_forward_result_default_path():
    result = _get_mock_result()
    attached = attach_attribution_to_walk_forward_result(result)

    assert "attribution_metadata" in attached
    assert "window_0" in attached["attribution_metadata"]["window_reviews"]
    assert "window_1" in attached["attribution_metadata"]["window_reviews"]
