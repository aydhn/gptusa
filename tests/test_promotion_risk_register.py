def test_risk_register():
    from usa_signal_bot.paper_promotion_dossier.risk_register import build_promotion_risk_register
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    risks = build_promotion_risk_register(d, [])
    assert isinstance(risks, list)
