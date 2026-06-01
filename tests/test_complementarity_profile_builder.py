import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.complementarity_profile_builder import build_complementarity_profiles
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references

def test_build_comp():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(2)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(2)]
    cands = build_ensemble_candidate_references(reports, validations)

    profs = build_complementarity_profiles(cands)
    assert len(profs) == 2
