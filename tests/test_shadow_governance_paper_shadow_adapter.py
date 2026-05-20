def test_adapter_ps():
    from usa_signal_bot.paper_shadow_governance.paper_shadow_adapter import comparison_from_shadow_sessions
    r = comparison_from_shadow_sessions({}, {})
    assert r is not None
