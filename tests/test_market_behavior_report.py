from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_report import (
    build_market_behavior_context, build_market_behavior_full_review
)

def test_build_market_behavior_context():
    ctx = build_market_behavior_context()
    assert ctx.status.value == "CREATED"

def test_build_market_behavior_full_review():
    rev = build_market_behavior_full_review()
    assert rev.report_type.value == "FULL_PHASE130_REVIEW"
