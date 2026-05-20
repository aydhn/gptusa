def test_adapter_pr():
    from usa_signal_bot.paper_shadow_governance.paper_runtime_adapter import attach_shadow_governance_to_paper_analytics
    from usa_signal_bot.paper_shadow_governance.comparison_report import build_shadow_governance_review
    rev = build_shadow_governance_review({}, {})
    res = attach_shadow_governance_to_paper_analytics({}, rev)
    assert "shadow_governance" in res
    assert not res["paper_order_executed"]
