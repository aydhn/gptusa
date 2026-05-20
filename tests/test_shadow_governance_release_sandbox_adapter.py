def test_adapter_rs():
    from usa_signal_bot.paper_shadow_governance.release_sandbox_adapter import shadow_comparison_from_sandbox_reviews
    r = shadow_comparison_from_sandbox_reviews({}, {})
    assert r is not None
