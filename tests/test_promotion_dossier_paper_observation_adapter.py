def test_adapter_pob():
    from usa_signal_bot.paper_promotion_dossier.paper_observation_adapter import attach_promotion_dossier_to_observation_payload
    class DummyReview: review_id = "R1"
    assert attach_promotion_dossier_to_observation_payload({}, DummyReview())["promotion_dossier_review_id"] == "R1"
