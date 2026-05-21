def test_readiness_package():
    from usa_signal_bot.paper_promotion_dossier.readiness_package import build_staged_paper_readiness_package
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    from usa_signal_bot.paper_promotion_dossier.safety_board_decision import FinalSafetyBoardDecisionEngine
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    engine = FinalSafetyBoardDecisionEngine()
    review = engine.decide(d, [])
    p = build_staged_paper_readiness_package(d, review)
    assert p.allowed_for_active_paper is False
