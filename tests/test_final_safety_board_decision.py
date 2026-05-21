def test_decision():
    from usa_signal_bot.paper_promotion_dossier.safety_board_decision import FinalSafetyBoardDecisionEngine
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    engine = FinalSafetyBoardDecisionEngine()
    review = engine.decide(d, [])
    assert review.allowed_for_active_paper is False
