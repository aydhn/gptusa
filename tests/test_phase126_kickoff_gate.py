import pytest
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata
from usa_signal_bot.feature_engine.final_closure.engine_readiness_certificate import build_engine_readiness_certificate
from usa_signal_bot.feature_engine.final_closure.phase126_kickoff_gate import build_phase126_kickoff_gate, phase126_kickoff_passed

def test_phase126_kickoff_gate_pass():
    artifacts = build_final_artifact_references()
    for a in artifacts:
        a.available = True
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    cert = build_engine_readiness_certificate(manifest, seal)
    gate = build_phase126_kickoff_gate(manifest, seal, cert)

    assert phase126_kickoff_passed(gate) is True
    assert gate.ready_for_phase126 is True
    assert gate.activation_allowed is False
    assert gate.strategy_activation_allowed is False
    assert gate.deployment_allowed is False

def test_phase126_kickoff_gate_fail():
    artifacts = build_final_artifact_references()
    # Missing artifacts -> Invalid manifest -> Invalid seal -> Invalid cert -> Failed gate
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    cert = build_engine_readiness_certificate(manifest, seal)
    gate = build_phase126_kickoff_gate(manifest, seal, cert)

    assert phase126_kickoff_passed(gate) is False
