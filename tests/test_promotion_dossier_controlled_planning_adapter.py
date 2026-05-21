def test_adapter_cp():
    from usa_signal_bot.paper_promotion_dossier.controlled_planning_adapter import attach_promotion_dossier_to_controlled_planning_payload
    class DummyReview: review_id = "R1"
    assert attach_promotion_dossier_to_controlled_planning_payload({}, DummyReview())["promotion_dossier_review_id"] == "R1"
