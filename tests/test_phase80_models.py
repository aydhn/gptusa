from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview, FinalHandoffEvidenceRef,
    SealedReadinessArchiveManifest, PrePaperGovernanceCheckpoint,
    validate_final_handoff_review
)
from usa_signal_bot.core.enums import FinalHandoffReviewStatus, FinalHandoffDecision, SealedArchiveStatus, PrePaperCheckpointStatus, PrePaperCheckpointDecision
from usa_signal_bot.core.exceptions import FinalHandoffValidationError

def test_models():
    # FinalHandoffReview
    review = FinalHandoffReview(
        handoff_review_id="test",
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
    validate_final_handoff_review(review)

    # Active paper shouldn't be allowed
    review.allows_active_paper = True
    try:
        validate_final_handoff_review(review)
        assert False, "Should have raised validation error"
    except FinalHandoffValidationError:
        pass

if __name__ == "__main__":
    test_models()
    print("All Model tests passed!")
