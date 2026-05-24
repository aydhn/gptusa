import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_evidence_freeze import build_simulator_evidence_freeze_bundle

def test_build_simulator_evidence_freeze_bundle():
    payload = {
        "simulator_dossier_full_review": {"data": "yes"},
        "local_paper_admission_simulator_gate_dossier": {"data": "yes"},
        "simulator_acceptance_seal": {"data": "yes"},
        "sandbox_runtime_admission_blocker_events": {"data": "yes"},
        "sandbox_runtime_admission_blocker_rules": {"data": "yes"},
        "simulator_gate_full_review": {"data": "yes"},
        "rehearsal_replay_result": {"data": "yes"},
        "dry_admission_evidence_freeze": {"data": "yes"},
        "simulator_dossier_continuity": {"data": "yes"},
        "simulator_dossier_safety_report": {"data": "yes"},
        "validation_reports": {"data": "yes"},
        "audit_trails": {"data": "yes"}
    }
    bundle = build_simulator_evidence_freeze_bundle(payload)
    assert bundle.missing_evidence_count == 0
    assert bundle.frozen is True
    assert bundle.immutable is True

def test_build_simulator_evidence_freeze_bundle_missing():
    payload = {
        "simulator_dossier_full_review": {"data": "yes"}
    }
    bundle = build_simulator_evidence_freeze_bundle(payload)
    assert bundle.missing_evidence_count > 0
