def test_reporting():
    from usa_signal_bot.paper_shadow_governance.governance_reporting import shadow_governance_limitations_text
    t = shadow_governance_limitations_text()
    assert "NOT investment advice" in t
