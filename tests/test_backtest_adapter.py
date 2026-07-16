from usa_signal_bot.attribution.backtest_adapter import (
    AttributionReportType,
    AttributionReview,
    create_attribution_review_id,
    attribution_review_to_dict,
    normalize_backtest_trades,
    aggregate_pnl_by_dimension,
    AttributionDimension,
    build_attribution_scorecard
)

def test_dependencies():
    # Only test that dependencies imported in backtest_adapter.py
    # are accessible, since the module currently contains no specific logic
    # and only serves as an import adapter.
    assert AttributionReportType is not None
    assert AttributionDimension is not None
    assert AttributionReview is not None
    assert callable(create_attribution_review_id)
    assert callable(attribution_review_to_dict)
    assert callable(normalize_backtest_trades)
    assert callable(aggregate_pnl_by_dimension)
    assert callable(build_attribution_scorecard)
