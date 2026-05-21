def test_eligibility():
    from usa_signal_bot.paper_promotion_dossier.eligibility_checker import evaluate_promotion_dossier_eligibility
    from usa_signal_bot.core.enums import PromotionDossierDecision
    assert evaluate_promotion_dossier_eligibility({"decision": "ELIGIBLE_FOR_NON_EXECUTING_PROMOTION_DOSSIER"}) == PromotionDossierDecision.CREATE_DOSSIER
