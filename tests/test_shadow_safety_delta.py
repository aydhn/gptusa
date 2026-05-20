def test_safety_delta():
    from usa_signal_bot.paper_shadow_governance.safety_delta import calculate_shadow_safety_delta
    d = calculate_shadow_safety_delta({"safety_flags": []}, {"safety_flags": []})
    assert d["increased"] is False
