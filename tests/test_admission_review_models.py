import pytest
from usa_signal_bot.paper_admission_review.admission_review_models import (
    PaperModeAdmissionReview,
    AdmissionReviewGate,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    FinalNoWriteTransitionCheckpoint,
    validate_paper_mode_admission_review,
    validate_ledger_reconciliation_report,
    validate_admission_evidence_seal,
    validate_final_no_write_transition_checkpoint
)
from usa_signal_bot.core.enums import PaperModeAdmissionReviewStatus, PaperModeAdmissionReviewDecision, AdmissionReviewGateStatus, LedgerReconciliationStatus, LedgerReconciliationDecision, NoWriteTransitionCheckpointStatus, NoWriteTransitionCheckpointDecision, AdmissionEvidenceSealStatus
from usa_signal_bot.core.exceptions import AdmissionReviewValidationError

def test_validate_paper_mode_admission_review():
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
    validate_paper_mode_admission_review(review)

    review.activation_denied = False
    with pytest.raises(AdmissionReviewValidationError):
        validate_paper_mode_admission_review(review)

def test_validate_ledger_reconciliation_report():
    report = LedgerReconciliationReport(
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
    validate_ledger_reconciliation_report(report)

    report.acknowledged_not_activation = False
    with pytest.raises(AdmissionReviewValidationError):
        validate_ledger_reconciliation_report(report)

def test_validate_admission_evidence_seal():
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
    validate_admission_evidence_seal(seal)

    seal.immutable = False
    with pytest.raises(AdmissionReviewValidationError):
        validate_admission_evidence_seal(seal)

def test_validate_final_no_write_transition_checkpoint():
    checkpoint = FinalNoWriteTransitionCheckpoint(
        checkpoint_id="test",
        created_at_utc="test",
        status=NoWriteTransitionCheckpointStatus.VALIDATED_NO_WRITE,
        decision=NoWriteTransitionCheckpointDecision.CONTINUE_TO_NO_WRITE_TRANSITION_DOSSIER,
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
        required_followups=[],
        safety_flags=[],
        warnings=[],
        errors=[]
    )
    validate_final_no_write_transition_checkpoint(checkpoint)

    checkpoint.transition_allowed = True
    with pytest.raises(AdmissionReviewValidationError):
        validate_final_no_write_transition_checkpoint(checkpoint)
