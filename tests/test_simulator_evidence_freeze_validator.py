import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_evidence_freeze_validator import validate_simulator_evidence_freeze_bundle_safety
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_evidence_freeze import build_simulator_evidence_freeze_bundle

def test_validate_simulator_evidence_freeze_bundle():
    payload = {
        "simulator_dossier_full_review": {"data": "yes"}
    }
    bundle = build_simulator_evidence_freeze_bundle(payload)
    errors = validate_simulator_evidence_freeze_bundle_safety(bundle)
    assert len(errors) > 0
    assert any("missing" in e.lower() for e in errors)
