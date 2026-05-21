def test_store():
    from usa_signal_bot.paper_promotion_dossier.dossier_store import promotion_dossier_store_summary
    from pathlib import Path
    res = promotion_dossier_store_summary(Path("data"))
    assert "dossiers" in res
