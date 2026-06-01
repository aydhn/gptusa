from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_builder import build_ensemble_prototype_specs

def test_build_ensemble_prototype_specs():
    groups = [{"candidate_group_id": "g1"}]
    blend_plans = [{"candidate_group_id": "g1", "blend_plan_id": "bp1", "blend_plan_name": "Test Blend", "coefficient_by_candidate_ref_id": {"c1": 0.6, "c2": 0.4}}]
    specs = build_ensemble_prototype_specs(groups, blend_plans)

    assert len(specs) == 1
    assert specs[0].coefficient_sum == 1.0
    assert specs[0].offline_evaluation_only is True
    assert specs[0].produces_trade_signal is False
