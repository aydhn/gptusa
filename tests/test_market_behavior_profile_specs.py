from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_profile_specs import (
    build_default_market_behavior_profile_specs, validate_market_behavior_profile_specs
)

def test_build_default_market_behavior_profile_specs():
    specs = build_default_market_behavior_profile_specs()
    assert len(specs) >= 7
    names = [s.profile_name for s in specs]
    assert "transition_behavior_profile" in names

def test_validate_market_behavior_profile_specs():
    specs = build_default_market_behavior_profile_specs()
    errs = validate_market_behavior_profile_specs(specs)
    assert not errs

    specs[0].produces_trade_signal = True
    errs = validate_market_behavior_profile_specs(specs)
    assert len(errs) > 0
