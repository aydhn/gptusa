import pytest
from usa_signal_bot.attribution.walk_forward_adapter import (
    build_attribution_by_walk_forward_window, attach_attribution_to_walk_forward_result
)

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
