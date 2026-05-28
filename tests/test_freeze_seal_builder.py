import pytest
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata, freeze_seal_valid

def test_freeze_seal_builder():
    artifacts = build_final_artifact_references()
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)

    assert seal.immutable is True
    assert seal.activation_allowed is False
    # Manifest will be invalid if required artifacts are missing, but the seal object is built.
    # In this case missing_required_artifacts > 0, so sealed should be False
    assert seal.sealed is False
    assert freeze_seal_valid(seal) is False # Not sealed

def test_freeze_seal_builder_valid():
    artifacts = build_final_artifact_references()
    for a in artifacts:
        a.available = True
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)

    assert seal.sealed is True
    assert freeze_seal_valid(seal) is True
