def test_dossier_builder():
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1", "decision": "ELIGIBLE_FOR_NON_EXECUTING_PROMOTION_DOSSIER"})
    assert d.candidate_id == "CAND-1"
    assert d.allowed_for_active_paper is False
