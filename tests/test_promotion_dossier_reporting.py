def test_reporting():
    from usa_signal_bot.paper_promotion_dossier.dossier_reporting import promotion_dossier_limitations_text
    assert "LIMITATIONS" in promotion_dossier_limitations_text()
