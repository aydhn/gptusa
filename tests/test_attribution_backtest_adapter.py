import pytest
from usa_signal_bot.attribution.backtest_adapter import (
    build_attribution_review_from_backtest_result,
    attach_attribution_to_backtest_result,
    backtest_attribution_summary,
    backtest_attribution_warnings
)
from usa_signal_bot.attribution.attribution_models import AttributionReview, AttributionScorecard

class DummyEnum:
    def __init__(self, value):
        self.value = value

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

def test_attach_attribution_to_backtest_result_with_review():
    result = _get_mock_result()
    scorecard = AttributionScorecard(
        scorecard_id="sc_123",
        created_at_utc="2023-01-01T00:00:00Z",
        total_gross_pnl_usd=100.0,
        total_net_pnl_usd=90.0,
        total_cost_usd=10.0,
        total_trade_count=1,
        positive_contributor_count=1,
        negative_contributor_count=0,
        detrimental_signal_count=0,
        high_risk_contributor_count=0,
        attribution_quality=DummyEnum("HIGH"),
        summary_scores={"alpha": 1.5},
        warnings=["Test warning"]
    )
    review = AttributionReview(
        review_id="rev_123",
        created_at_utc="2023-01-01T00:00:00Z",
        report_type=DummyEnum("PERFORMANCE_ATTRIBUTION"),
        events=[],
        performance_contributions=[],
        risk_contributions=[],
        signal_contributions=[],
        scorecard=scorecard,
        warnings=["Test warning"]
    )

    attached = attach_attribution_to_backtest_result(result, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "rev_123"
    assert attached["attribution_metadata"]["scorecard"] == {"alpha": 1.5}
    assert attached["attribution_metadata"]["warnings"] == ["Test warning"]

def test_attach_attribution_to_backtest_result_with_review_no_scorecard():
    result = _get_mock_result()
    review = AttributionReview(
        review_id="rev_123",
        created_at_utc="2023-01-01T00:00:00Z",
        report_type=DummyEnum("PERFORMANCE_ATTRIBUTION"),
        events=[],
        performance_contributions=[],
        risk_contributions=[],
        signal_contributions=[],
        scorecard=None,
        warnings=["Test warning"]
    )

    attached = attach_attribution_to_backtest_result(result, review)
    assert "attribution_metadata" in attached
    assert attached["attribution_metadata"]["review_id"] == "rev_123"
    assert attached["attribution_metadata"]["scorecard"] == {}
    assert attached["attribution_metadata"]["warnings"] == ["Test warning"]

def test_backtest_attribution_summary():
    # Test with metadata
    result = {"attribution_metadata": {"review_id": "rev_123", "scorecard": {"alpha": 1.5}}}
    summary = backtest_attribution_summary(result)
    assert summary == {"review_id": "rev_123", "scorecard": {"alpha": 1.5}}

    # Test without metadata
    result = {}
    summary = backtest_attribution_summary(result)
    assert summary == {}

def test_backtest_attribution_warnings():
    # Test with warnings
    result = {"attribution_metadata": {"warnings": ["Warning 1", "Warning 2"]}}
    warnings = backtest_attribution_warnings(result)
    assert warnings == ["Warning 1", "Warning 2"]

    # Test without warnings
    result = {"attribution_metadata": {}}
    warnings = backtest_attribution_warnings(result)
    assert warnings == []

    # Test without metadata
    result = {}
    warnings = backtest_attribution_warnings(result)
    assert warnings == []
