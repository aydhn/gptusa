def test_adapter_pr():
    from usa_signal_bot.paper_promotion_dossier.paper_runtime_adapter import build_read_only_paper_runtime_snapshot_for_promotion_dossier
    assert build_read_only_paper_runtime_snapshot_for_promotion_dossier()["read_only"] is True
