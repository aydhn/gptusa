def test_validation():
    from usa_signal_bot.paper_promotion_dossier.dossier_validation import validate_no_live_execution_language_in_promotion_dossier
    r = validate_no_live_execution_language_in_promotion_dossier("sent to broker")
    assert r.valid is False
