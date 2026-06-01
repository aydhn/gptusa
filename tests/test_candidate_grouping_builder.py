import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references
from usa_signal_bot.ml_research.ensemble_scaffolding.candidate_grouping_builder import build_candidate_groups

def test_build_groups():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(5)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(5)]
    cands = build_ensemble_candidate_references(reports, validations)

    groups = build_candidate_groups(cands, max_group_size=3)
    assert len(groups) == 3
    assert groups[0].actual_candidate_count == 3
    for g in groups:
        assert g.eligible_for_live_use is False
