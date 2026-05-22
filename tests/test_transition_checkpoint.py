from usa_signal_bot.core.enums import PaperModeAdmissionReviewStatus, PaperModeAdmissionReviewDecision
from usa_signal_bot.paper_admission_review.admission_review_models import PaperModeAdmissionReview, LedgerReconciliationReport, AdmissionEvidenceSeal
from usa_signal_bot.paper_admission_review.transition_checkpoint import build_final_no_write_transition_checkpoint
from usa_signal_bot.core.enums import LedgerReconciliationStatus, LedgerReconciliationDecision, AdmissionEvidenceSealStatus, NoWriteTransitionCheckpointStatus, NoWriteTransitionCheckpointDecision

def test_build_final_no_write_transition_checkpoint():
    review = PaperModeAdmissionReview(
        admission_review_id="test",
        created_at_utc="test",
        status=PaperModeAdmissionReviewStatus.READY,
        decision=PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT,
        gates=[],
        evidence_refs=[],
        required_followups=[],
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        transition_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        warnings=[],
        errors=[]
    )
    reconciliation = LedgerReconciliationReport(
        reconciliation_id="test",
        created_at_utc="test",
        status=LedgerReconciliationStatus.RECONCILED,
        decision=LedgerReconciliationDecision.ACCEPT_NO_WRITE_ACKNOWLEDGEMENT,
        items=[],
        required_scopes=[],
        completed_scopes=[],
        missing_scopes=[],
        acknowledged_no_write=True,
        acknowledged_not_activation=True,
        activation_allowed=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )
    seal = AdmissionEvidenceSeal(
        seal_id="test",
        created_at_utc="test",
        status=AdmissionEvidenceSealStatus.SEALED,
        evidence_refs=["ref1"],
        sealed=True,
        immutable=True,
        warnings=[],
        errors=[],
        seal_hash="hash"
    )

    checkpoint = build_final_no_write_transition_checkpoint(review, reconciliation, seal)
    assert checkpoint.status == NoWriteTransitionCheckpointStatus.VALIDATED_NO_WRITE
    assert checkpoint.decision == NoWriteTransitionCheckpointDecision.CONTINUE_TO_NO_WRITE_TRANSITION_DOSSIER
    assert checkpoint.activation_denied
    assert not checkpoint.activation_allowed
