import pytest
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import *
from usa_signal_bot.paper_boundary_certificate.no_order_ingestion import *
from usa_signal_bot.paper_boundary_certificate.eligibility_checker import *
from usa_signal_bot.paper_boundary_certificate.blocker_replay_plan import *
from usa_signal_bot.paper_boundary_certificate.blocker_replay_engine import *
from usa_signal_bot.paper_boundary_certificate.blocker_replay_analyzer import *
from usa_signal_bot.paper_boundary_certificate.evidence_freeze import *
from usa_signal_bot.paper_boundary_certificate.evidence_freeze_validator import *
from usa_signal_bot.paper_boundary_certificate.boundary_rules import *
from usa_signal_bot.paper_boundary_certificate.boundary_assertions import *
from usa_signal_bot.paper_boundary_certificate.boundary_certificate import *
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_validator import *
from usa_signal_bot.paper_boundary_certificate.boundary_continuity import *
from usa_signal_bot.paper_boundary_certificate.boundary_safety_validator import *
from usa_signal_bot.paper_boundary_certificate.boundary_audit import *
from usa_signal_bot.paper_boundary_certificate.boundary_report import *
from usa_signal_bot.paper_boundary_certificate.boundary_validation import *
from usa_signal_bot.core.enums import PaperSandboxBoundaryDecision, AdmissionBlockerReplayOutcome, NoOrderEvidenceFreezeDecision

def test_models():
    plan = build_default_blocker_replay_plan()
    assert plan.require_all_attempts_blocked is True
    assert plan.execution_enabled is False

def test_no_order_ingestion():
    payload = {"dossier": {"dossier_id": "1"}, "bridge_replay_audit_seal": {"seal_id": "1"}, "admission_blocker_events": [{"blocked": True}]}
    assert no_order_supports_boundary_certificate(payload)[0] is True

def test_eligibility_checker():
    payload = {"dossier": {"dossier_id": "1"}, "bridge_replay_audit_seal": {"seal_id": "1"}, "admission_blocker_events": [{"blocked": True}]}
    assert evaluate_boundary_certificate_eligibility(payload) == PaperSandboxBoundaryDecision.CREATE_BOUNDARY_CERTIFICATE

def test_blocker_replay_engine():
    plan = build_default_blocker_replay_plan()
    engine = PaperAdmissionBlockerReplayEngine()
    result = engine.replay(plan, [{"blocked": True}])
    assert result.passed is True
    assert result.outcome == AdmissionBlockerReplayOutcome.ALL_ADMISSION_ATTEMPTS_BLOCKED

def test_evidence_freeze():
    bundle = build_no_order_evidence_freeze_bundle({"candidate_id": "test"})
    assert bundle.frozen is True
    assert bundle.immutable is True
    assert bundle.freeze_is_metadata_only is True

def test_boundary_rules():
    rules = build_boundary_rules({})
    assert len(rules) == 9

def test_boundary_assertions():
    assertions = build_boundary_assertions({})
    assert len(assertions) == 7

def test_boundary_certificate():
    cert = build_default_boundary_certificate()
    assert cert.sealed is True
    assert cert.immutable is True
    assert cert.activation_denied is True
    assert cert.activation_allowed is False
    assert cert.admission_allowed is False

def test_boundary_validation():
    cert = build_default_boundary_certificate()
    report = validate_boundary_certificate_report(cert)
    assert report.valid is True
