from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorProfile
from usa_signal_bot.regime_classification.behavior_reporting.regime_behavior_summary_builder import (
    build_regime_behavior_summaries, validate_regime_behavior_summaries
)

def test_build_regime_behavior_summaries():
    p = MarketBehaviorProfile(symbol="AAPL")
    sums = build_regime_behavior_summaries([p])
    assert len(sums) == 5
    assert sums[0].symbol == "AAPL"
    assert sums[0].title == "Transition Summary"

def test_validate_regime_behavior_summaries():
    p = MarketBehaviorProfile(symbol="AAPL")
    sums = build_regime_behavior_summaries([p])
    errs = validate_regime_behavior_summaries(sums)
    assert not errs
