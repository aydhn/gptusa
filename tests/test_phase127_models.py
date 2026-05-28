import pytest
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import (
    RegimeFoundationIngestionResult,
    RegimeCandidateScore,
    RegimeCandidateReadinessGate,
    RegimeCandidateReadinessStatus,
    validate_regime_foundation_ingestion_result,
    validate_regime_candidate_score,
    validate_regime_candidate_readiness_gate
)

def test_regime_foundation_ingestion_result_validation():
    res = RegimeFoundationIngestionResult(ready_for_phase127=True, research_data_only=True)
    validate_regime_foundation_ingestion_result(res)

    res.activation_allowed = True
    with pytest.raises(ValueError):
        validate_regime_foundation_ingestion_result(res)

def test_regime_candidate_score_validation():
    score = RegimeCandidateScore(candidate_score=50.0, normalized_candidate_score=0.5)
    validate_regime_candidate_score(score)

    score.candidate_score = 150.0
    with pytest.raises(ValueError):
        validate_regime_candidate_score(score)

def test_regime_candidate_readiness_gate_validation():
    gate = RegimeCandidateReadinessGate(ready_for_phase128=True, status=RegimeCandidateReadinessStatus.PASSED)
    validate_regime_candidate_readiness_gate(gate)

    gate.status = RegimeCandidateReadinessStatus.FAILED
    with pytest.raises(ValueError):
        validate_regime_candidate_readiness_gate(gate)
