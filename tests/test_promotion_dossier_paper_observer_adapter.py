def test_adapter_po():
    from usa_signal_bot.paper_promotion_dossier.paper_observer_adapter import attach_promotion_hint_to_paper_observer_payload
    assert "promotion_dossier_hint" in attach_promotion_hint_to_paper_observer_payload({}, None)
