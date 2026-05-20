def test_risk_delta():
    from usa_signal_bot.paper_shadow_governance.risk_delta import calculate_shadow_risk_delta
    d = calculate_shadow_risk_delta({}, {})
    assert "drawdown_delta" in d
