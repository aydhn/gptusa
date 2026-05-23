from usa_signal_bot.core.enums import PaperModeAdmissionReviewStatus, PaperModeAdmissionReviewDecision, AdmissionReviewRiskFlag
from usa_signal_bot.paper_admission_review.admission_review_models import PaperModeAdmissionReview
from usa_signal_bot.paper_admission_review.admission_safety_validator import validate_admission_safety, admission_has_blocking_flags

def test_validate_admission_safety():
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
    errors = validate_admission_safety(admission_review=review)
    assert len(errors) == 0

    review.activation_allowed = True
    errors = validate_admission_safety(admission_review=review)
    assert len(errors) > 0

def test_admission_has_blocking_flags():
    flags = [AdmissionReviewRiskFlag.BROKER_ORDER_RISK]
    assert admission_has_blocking_flags(flags)

    safe_flags = [AdmissionReviewRiskFlag.UNKNOWN]
    assert not admission_has_blocking_flags(safe_flags)
