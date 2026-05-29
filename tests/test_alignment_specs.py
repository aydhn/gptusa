from usa_signal_bot.regime_classification.alignment.alignment_specs import build_default_regime_alignment_specs, build_default_market_behavior_overlay_specs
def test_specs():
    a = build_default_regime_alignment_specs()
    assert len(a) >= 6
    o = build_default_market_behavior_overlay_specs()
    assert len(o) >= 6
