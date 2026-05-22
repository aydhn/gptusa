from usa_signal_bot.core.enums import PaperModeAdmissionReviewStatus, PaperModeAdmissionReviewDecision
from usa_signal_bot.paper_admission_review.admission_review_models import PaperModeAdmissionReview
from usa_signal_bot.paper_admission_review.admission_audit import audit_entry_from_admission_review, admission_audit_summary

def test_audit_entry_from_admission_review():
    review = PaperModeAdmissionReview(
        admission_review_id="test",
        created_at_utc="test",
        status=PaperModeAdmissionReviewStatus.READY,
        decision=PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT,
        gates=[],
        evidence_refs=["ref1"],
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
    entry = audit_entry_from_admission_review(review)
    assert entry.entity_type == "PaperModeAdmissionReview"
    assert entry.action == "Admission Review Processed"
    assert entry.decision == PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT

    summary = admission_audit_summary([entry])
    assert summary["total_entries"] == 1
