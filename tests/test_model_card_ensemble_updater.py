import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.model_card_ensemble_updater import update_model_card_with_ensemble_report
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_preparation_report import build_ensemble_preparation_reports
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references
from usa_signal_bot.ml_research.ensemble_scaffolding.candidate_grouping_builder import build_top_ranked_candidate_group
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_family_specs import build_simple_average_research_family
from usa_signal_bot.ml_research.ensemble_scaffolding.blend_policy_builder import build_equal_coefficient_policy
from usa_signal_bot.ml_research.ensemble_scaffolding.blend_coefficient_planner import build_equal_blend_coefficient_plan

def test_build_updater():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(2)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(2)]
    cands = build_ensemble_candidate_references(reports, validations)
    group = build_top_ranked_candidate_group(cands)
    fam = build_simple_average_research_family()
    pol = build_equal_coefficient_policy(group, fam.family_kind)
    plan = build_equal_blend_coefficient_plan(group, pol)
    reps = build_ensemble_preparation_reports([group], [fam], [pol], [plan], [], [], [], [])

    upd = update_model_card_with_ensemble_report(None, reps[0])
    assert upd.not_deployment_artifact is True
    assert upd.no_ensemble_fitting_performed is True
