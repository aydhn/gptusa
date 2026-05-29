from usa_signal_bot.regime_classification.alignment.cross_symbol_compatibility_profiles import build_cross_symbol_compatibility_profile
def test_cross_symbol():
    p = build_cross_symbol_compatibility_profile([])
    assert p.profile_name == "cross_symbol_profile"
