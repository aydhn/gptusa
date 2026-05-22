from usa_signal_bot.paper_final_handoff.final_handoff_models import *
from usa_signal_bot.paper_final_handoff.eligibility_checker import evaluate_final_handoff_eligibility
from usa_signal_bot.paper_final_handoff.archive_manifest import build_final_handoff_evidence_refs, build_sealed_readiness_archive_manifest
from usa_signal_bot.paper_final_handoff.archive_sealing import seal_readiness_archive, verify_archive_seal
from usa_signal_bot.paper_final_handoff.archive_integrity import build_archive_integrity_report
from usa_signal_bot.paper_final_handoff.checkpoint_gates import default_pre_paper_checkpoint_gates
from usa_signal_bot.paper_final_handoff.checkpoint_decision import PrePaperCheckpointDecisionEngine
from usa_signal_bot.paper_final_handoff.non_execution_compliance import validate_handoff_non_execution
from usa_signal_bot.paper_final_handoff.final_handoff_safety import validate_final_handoff_safety
from usa_signal_bot.paper_final_handoff.checkpoint_audit import create_final_handoff_audit_entry, audit_entry_from_handoff_review
from usa_signal_bot.paper_final_handoff.final_handoff_report import build_final_handoff_review, build_final_handoff_full_review
from usa_signal_bot.paper_final_handoff.readiness_rehearsal_adapter import final_handoff_full_review_from_readiness_rehearsal
from usa_signal_bot.paper_final_handoff.promotion_dossier_adapter import final_handoff_evidence_from_promotion_dossier
from usa_signal_bot.paper_final_handoff.observer_governance_adapter import final_handoff_evidence_from_observer_governance
from usa_signal_bot.paper_final_handoff.paper_runtime_adapter import build_read_only_paper_snapshot_for_final_handoff
from usa_signal_bot.paper_final_handoff.final_handoff_validation import validate_no_live_execution_language_in_final_handoff
from usa_signal_bot.core.enums import FinalHandoffDecision, FinalHandoffReviewStatus, PrePaperCheckpointDecision

def test_eligibility_checker():
    # Incomplete payload -> BLOCK or REQUEST_HANDOFF_REHEARSAL_RERUN depending on missing lock
    res = evaluate_final_handoff_eligibility({})
    assert res == FinalHandoffDecision.REQUEST_HANDOFF_REHEARSAL_RERUN

    # Payload with block status
    res = evaluate_final_handoff_eligibility({"status": "BLOCKED"})
    assert res == FinalHandoffDecision.BLOCK

    # Valid payload
    payload = {
        "status": "READY_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW",
        "final_review_lock": {"id": "1"},
        "guarded_handoff_registry_entry": {"status": "REGISTERED", "allows_active_paper": False},
        "manual_review_completed": True,
        "evidence_valid": True
    }
    res = evaluate_final_handoff_eligibility(payload)
    assert res == FinalHandoffDecision.CREATE_SEALED_READINESS_ARCHIVE

def test_archive_manifest_and_sealing():
    review = FinalHandoffReview(
        handoff_review_id="test_review",
        created_at_utc="now",
        status=FinalHandoffReviewStatus.COMPLETED,
        candidate_id="c1",
        source_handoff_id="h1",
        source_rehearsal_run_id="r1",
        source_final_lock_id="l1",
        evidence_refs=[],
        decision=FinalHandoffDecision.CREATE_SEALED_READINESS_ARCHIVE,
        safety_flags=[],
        manual_review_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    manifest = build_sealed_readiness_archive_manifest(review)
    assert not manifest.sealed
    assert not manifest.immutable

    sealed = seal_readiness_archive(manifest)
    assert sealed.sealed
    assert sealed.immutable
    assert sealed.archive_hash is not None
    assert verify_archive_seal(sealed)

    # Integrity report
    report = build_archive_integrity_report(sealed)
    assert report.status.value == "PASS"

def test_checkpoint_gates_and_decision():
    review = FinalHandoffReview(
        handoff_review_id="test_review",
        created_at_utc="now",
        status=FinalHandoffReviewStatus.COMPLETED,
        candidate_id="c1",
        source_handoff_id="h1",
        source_rehearsal_run_id="r1",
        source_final_lock_id="l1",
        evidence_refs=[],
        decision=FinalHandoffDecision.CREATE_SEALED_READINESS_ARCHIVE,
        safety_flags=[],
        manual_review_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    manifest = build_sealed_readiness_archive_manifest(review)
    sealed = seal_readiness_archive(manifest)
    integrity = build_archive_integrity_report(sealed)

    gates = default_pre_paper_checkpoint_gates(review, sealed, integrity)
    assert len(gates) == 9

    engine = PrePaperCheckpointDecisionEngine()
    decision = engine.decide(review, sealed, integrity, gates)
    assert decision.decision == PrePaperCheckpointDecision.PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL
    assert not decision.allows_active_paper

def test_validation_and_safety():
    review = FinalHandoffReview(
        handoff_review_id="test_review",
        created_at_utc="now",
        status=FinalHandoffReviewStatus.COMPLETED,
        candidate_id="c1",
        source_handoff_id="h1",
        source_rehearsal_run_id="r1",
        source_final_lock_id="l1",
        evidence_refs=[],
        decision=FinalHandoffDecision.CREATE_SEALED_READINESS_ARCHIVE,
        safety_flags=[],
        manual_review_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    compliance = validate_handoff_non_execution(review)
    assert compliance["valid"]

    safety_errors = validate_final_handoff_safety(review)
    assert len(safety_errors) == 0

def test_language_validation():
    # Test that we block live execution language
    report = validate_no_live_execution_language_in_final_handoff("Everything looks good, live approved")
    assert not report.valid
    assert len(report.issues) == 1

    report2 = validate_no_live_execution_language_in_final_handoff("Ready for non-executing handoff")
    assert report2.valid

def test_adapters():
    dossier_payload = {"dossier_id": "d1"}
    evs = final_handoff_evidence_from_promotion_dossier(dossier_payload)
    assert len(evs) == 1
    assert evs[0].source_type == "promotion_dossier"

    snapshot = build_read_only_paper_snapshot_for_final_handoff(None)
    assert snapshot["paper_state_committed"] == False

if __name__ == "__main__":
    test_eligibility_checker()
    test_archive_manifest_and_sealing()
    test_checkpoint_gates_and_decision()
    test_validation_and_safety()
    test_language_validation()
    test_adapters()
    print("All additional tests passed!")
