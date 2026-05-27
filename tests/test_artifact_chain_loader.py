import pytest
from usa_signal_bot.feature_engine.integration_freeze.artifact_chain_loader import build_expected_artifact_chain, ArtifactChainPhase

def test_build_expected_artifact_chain():
    chain = build_expected_artifact_chain()
    assert len(chain) == 8
    phases = [r.phase for r in chain]
    assert ArtifactChainPhase.PHASE_116_FEATURE_FOUNDATION in phases
    assert ArtifactChainPhase.PHASE_123_FACTOR_EXPLAINABILITY in phases
