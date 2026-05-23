from usa_signal_bot.core.enums import PaperModeAdmissionReviewDecision
from usa_signal_bot.paper_admission_review.admission_decision import GuardedPaperModeAdmissionReviewDecisionEngine

def test_admission_decision_engine():
    engine = GuardedPaperModeAdmissionReviewDecisionEngine()
    payload = {
        "activation_allowed": True
    }
    decision = engine.decide(payload, [])
    assert decision.decision == PaperModeAdmissionReviewDecision.BLOCK

    clean_payload = {
        "activation_allowed": False,
        "all_writes_blocked": True,
        "mutation_detected": False,
        "dry_admission_run": {"status": "COMPLETED_NO_WRITE"},
        "write_lock_refresh": {"status": "VALIDATED"}
    }
    from usa_signal_bot.paper_admission_review.admission_review_models import LedgerReconciliationReport
    from usa_signal_bot.core.enums import LedgerReconciliationStatus, LedgerReconciliationDecision
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
    decision = engine.decide(clean_payload, [], reconciliation=reconciliation)
    assert decision.decision == PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT
