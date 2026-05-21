def test_compliance():
    from usa_signal_bot.paper_promotion_dossier.non_execution_compliance import validate_dossier_non_execution
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    res = validate_dossier_non_execution(d)
    assert res["valid"] is True
