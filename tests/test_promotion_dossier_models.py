def test_models_import():
    import usa_signal_bot.paper_promotion_dossier.dossier_models as dm
    assert dm.PromotionEvidenceIndex is not None
