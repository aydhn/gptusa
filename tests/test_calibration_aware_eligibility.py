import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.calibration_aware_eligibility import build_calibration_aware_eligibility_profiles
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references

def test_build_elig():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(2)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(2)]
    cands = build_ensemble_candidate_references(reports, validations)

    profs = build_calibration_aware_eligibility_profiles(cands, reports)
    assert len(profs) == 2
    for p in profs:
        assert p.eligible_for_phase143_research is True
        assert p.live_use_allowed is False
