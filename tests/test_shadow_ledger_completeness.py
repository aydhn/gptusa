def test_ledger():
    from usa_signal_bot.paper_shadow_governance.ledger_completeness import check_shadow_ledger_completeness
    d = check_shadow_ledger_completeness({})
    assert not d["complete"]
