import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references

def test_build_candidates():
    reports = [{"candidate_id": "cand_1", "reliability_score": 0.9}]
    validations = [{"candidate_id": "cand_1", "passed": True}]
    preds = [{"candidate_id": "cand_1", "artifact_id": "art_1"}]

    cands = build_ensemble_candidate_references(reports, validations, preds)
    assert len(cands) == 1
    assert cands[0].source_candidate_id == "cand_1"
    assert cands[0].eligible_for_ensemble_research is True
    assert cands[0].prediction_artifact_id == "art_1"

def test_build_candidates_failed_validation():
    reports = [{"candidate_id": "cand_1", "reliability_score": 0.9}]
    validations = [{"candidate_id": "cand_1", "passed": False}]

    cands = build_ensemble_candidate_references(reports, validations)
    assert cands[0].eligible_for_ensemble_research is False
