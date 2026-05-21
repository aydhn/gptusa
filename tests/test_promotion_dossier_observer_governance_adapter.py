def test_adapter_og():
    from usa_signal_bot.paper_promotion_dossier.observer_governance_adapter import attach_promotion_dossier_metadata_to_observer_governance
    class DummyReview: review_id = "R1"
    assert attach_promotion_dossier_metadata_to_observer_governance({}, DummyReview())["promotion_dossier_review_id"] == "R1"
