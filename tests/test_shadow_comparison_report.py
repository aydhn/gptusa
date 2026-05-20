def test_comparison_report():
    from usa_signal_bot.paper_shadow_governance.comparison_report import build_shadow_governance_review
    r = build_shadow_governance_review({}, {})
    assert len(r.comparison_reports) == 1
