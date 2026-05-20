def test_adapter_rg():
    from usa_signal_bot.paper_shadow_governance.research_governance_adapter import attach_shadow_governance_to_research_governance_payload
    from usa_signal_bot.paper_shadow_governance.comparison_report import build_shadow_governance_review
    rev = build_shadow_governance_review({}, {})
    res = attach_shadow_governance_to_research_governance_payload({}, rev)
    assert "shadow_governance" in res
