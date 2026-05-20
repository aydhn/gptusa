def test_adapter_rp():
    from usa_signal_bot.paper_shadow_governance.release_packaging_adapter import shadow_governance_from_bundle_payloads
    r = shadow_governance_from_bundle_payloads({}, {})
    assert r is not None
