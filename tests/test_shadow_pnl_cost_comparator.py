def test_pnl_cost():
    from usa_signal_bot.paper_shadow_governance.pnl_cost_comparator import compare_shadow_pnl_cost
    d = compare_shadow_pnl_cost({}, {})
    assert "pnl_delta" in d
