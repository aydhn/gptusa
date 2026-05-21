def test_stage_plans():
    from usa_signal_bot.paper_promotion_dossier.readiness_stage_plan import default_readiness_stage_plans
    from usa_signal_bot.paper_promotion_dossier.dossier_builder import build_promotion_dossier_from_observer_governance
    d = build_promotion_dossier_from_observer_governance({"candidate_id": "CAND-1"})
    plans = default_readiness_stage_plans(d)
    assert len(plans) == 4
