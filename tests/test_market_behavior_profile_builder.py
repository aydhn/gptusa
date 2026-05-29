from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_profile_builder import (
    build_market_behavior_profiles, validate_market_behavior_profiles
)
from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_profile_specs import build_default_market_behavior_profile_specs

def test_build_market_behavior_profiles():
    tm = [{"symbol": "AAPL", "dominant_transition": "bull_to_bear"}]
    pp = [{"symbol": "AAPL", "median_run_length": 15}]
    dp = [{"symbol": "AAPL", "average_duration": 20}]
    cd = [{"symbol": "AAPL", "churn_level": "LOW"}]
    sd = [{"symbol": "AAPL", "stability_score": 85.0}]

    specs = build_default_market_behavior_profile_specs()
    profs = build_market_behavior_profiles(tm, pp, dp, cd, sd, specs)

    # Excludes cross symbol for now
    assert len(profs) == 6
    assert profs[0].symbol == "AAPL"

def test_validate_market_behavior_profiles():
    tm = [{"symbol": "AAPL", "dominant_transition": "bull_to_bear"}]
    profs = build_market_behavior_profiles(tm, [], [], [], [])
    errs = validate_market_behavior_profiles(profs)
    assert not errs
