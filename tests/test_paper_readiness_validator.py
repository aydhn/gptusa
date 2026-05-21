def test_readiness_snapshot():
    from usa_signal_bot.paper_promotion_dossier.paper_readiness_validator import build_read_only_paper_readiness_snapshot
    s = build_read_only_paper_readiness_snapshot({"a": 1})
    assert s["read_only"] is True
