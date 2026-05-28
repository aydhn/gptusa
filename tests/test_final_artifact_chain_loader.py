import pytest
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references, validate_final_artifact_references

def test_final_artifact_chain_loader():
    refs = build_final_artifact_references()
    assert len(refs) > 0
    errs = validate_final_artifact_references(refs)
    assert len(errs) > 0  # because they are available=False by default
