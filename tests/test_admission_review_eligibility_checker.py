from usa_signal_bot.core.enums import PaperModeAdmissionReviewDecision
from usa_signal_bot.paper_admission_review.eligibility_checker import evaluate_admission_review_eligibility

def test_evaluate_admission_review_eligibility():
    payload = {
        "activation_allowed": True,
        "all_writes_blocked": False,
        "mutation_detected": True,
    }
    decision = evaluate_admission_review_eligibility(payload)
    assert decision == PaperModeAdmissionReviewDecision.BLOCK

    clean_payload = {
        "activation_allowed": False,
        "all_writes_blocked": True,
        "mutation_detected": False,
        "dry_admission_run": {"status": "COMPLETED_NO_WRITE"},
        "human_approval_ledger": {"missing_scopes": []},
        "write_lock_refresh": {"status": "VALIDATED"}
    }
    decision = evaluate_admission_review_eligibility(clean_payload)
    assert decision == PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT
