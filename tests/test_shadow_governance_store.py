def test_store(tmp_path):
    from usa_signal_bot.paper_shadow_governance.governance_store import shadow_governance_store_summary
    res = shadow_governance_store_summary(tmp_path)
    assert res["total_reviews"] == 0
