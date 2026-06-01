import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.blend_policy_builder import build_equal_coefficient_policy
from usa_signal_bot.ml_research.ensemble_scaffolding.candidate_grouping_builder import build_top_ranked_candidate_group
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references

def test_build_policy():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(2)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(2)]
    cands = build_ensemble_candidate_references(reports, validations)
    group = build_top_ranked_candidate_group(cands)

    pol = build_equal_coefficient_policy(group)
    assert pol.coefficient_sum_required == 1.0
    assert pol.fitting_allowed_in_phase142 is False
