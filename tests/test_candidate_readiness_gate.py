import pytest
from usa_signal_bot.regime_classification.feature_engineering.candidate_readiness_gate import (
    build_candidate_readiness_gate
)
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import (
    RegimeFoundationIngestionResult,
    RegimeCandidatePreparationResult,
    RegimeCandidateDefinition
)

def test_build_candidate_readiness_gate():
    ing = RegimeFoundationIngestionResult(valid_for_phase127=True)
    prep = RegimeCandidatePreparationResult()
    prep.candidate_definitions = [RegimeCandidateDefinition()]
    prep.candidates_valid = True

    gate = build_candidate_readiness_gate(ing, [], prep)

    assert gate.ready_for_phase128 is True
    assert gate.model_training_used is False
    assert gate.produces_trade_signal is False
