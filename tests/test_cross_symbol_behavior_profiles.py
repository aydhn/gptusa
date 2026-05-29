from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorProfile
from usa_signal_bot.regime_classification.behavior_reporting.cross_symbol_behavior_profiles import (
    build_cross_symbol_behavior_profile, validate_cross_symbol_behavior_profile
)

def test_build_cross_symbol_behavior_profile():
    p1 = MarketBehaviorProfile(symbol="AAPL", dominant_regime_label="bull")
    p2 = MarketBehaviorProfile(symbol="MSFT", dominant_regime_label="bear")
    p3 = MarketBehaviorProfile(symbol="GOOG", dominant_regime_label="bull")
    prof = build_cross_symbol_behavior_profile([p1, p2, p3])

    assert prof.profile_name == "cross_symbol_behavior_profile"
    assert prof.metric_snapshot["distribution"]["bull"] == 2
    assert prof.metric_snapshot["distribution"]["bear"] == 1

def test_validate_cross_symbol_behavior_profile():
    p1 = MarketBehaviorProfile(symbol="AAPL", dominant_regime_label="bull")
    prof = build_cross_symbol_behavior_profile([p1])
    errs = validate_cross_symbol_behavior_profile(prof)
    assert not errs
