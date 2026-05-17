import pytest
from usa_signal_bot.attribution.backtest_adapter import (
    build_attribution_review_from_backtest_result, attach_attribution_to_backtest_result
)

def _get_mock_result():
    return {
        "summary": {"total_pnl": 100},
        "trades": [
            {"symbol": "AAPL", "net_pnl_usd": 100.0, "total_cost_usd": 10.0, "strategy_name": "Trend"}
        ]
    }

def test_build_attribution_review_from_backtest_result():
    result = _get_mock_result()
    review = build_attribution_review_from_backtest_result(result)
    assert len(review.events) == 1
    assert review.events[0].symbol == "AAPL"
    assert review.scorecard.total_net_pnl_usd == 100.0

def test_attach_attribution_to_backtest_result():
    result = _get_mock_result()
    attached = attach_attribution_to_backtest_result(result)
    assert "attribution_metadata" in attached
    assert "review_id" in attached["attribution_metadata"]
