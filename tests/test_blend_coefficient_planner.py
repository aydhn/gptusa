import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.blend_coefficient_planner import build_equal_blend_coefficient_plan
from usa_signal_bot.ml_research.ensemble_scaffolding.blend_policy_builder import build_equal_coefficient_policy
from usa_signal_bot.ml_research.ensemble_scaffolding.candidate_grouping_builder import build_top_ranked_candidate_group
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references

def test_build_plan():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(2)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(2)]
    cands = build_ensemble_candidate_references(reports, validations)
    group = build_top_ranked_candidate_group(cands)
    pol = build_equal_coefficient_policy(group)

    plan = build_equal_blend_coefficient_plan(group, pol)
    assert plan.coefficient_valid is True
    assert plan.not_portfolio_weight is True
    assert plan.fitting_performed is False
    assert abs(plan.coefficient_sum - 1.0) < 1e-6
