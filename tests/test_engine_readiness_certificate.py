import pytest
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata
from usa_signal_bot.feature_engine.final_closure.engine_readiness_certificate import build_engine_readiness_certificate, engine_certificate_valid

def test_engine_readiness_certificate():
    artifacts = build_final_artifact_references()
    for a in artifacts:
        a.available = True
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    cert = build_engine_readiness_certificate(manifest, seal)

    assert cert.certified_for_research_handoff is True
    assert cert.certified_for_trading_activation is False
    assert cert.certified_for_deployment is False
    assert engine_certificate_valid(cert) is True
