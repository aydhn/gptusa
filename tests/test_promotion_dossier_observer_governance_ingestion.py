def test_ingestion():
    from usa_signal_bot.paper_promotion_dossier.observer_governance_ingestion import ingest_observer_governance_review
    assert ingest_observer_governance_review({"test": 1}) == {"test": 1}
