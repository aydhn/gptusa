from usa_signal_bot.paper_readiness_confirmation.eligibility_checker import (
    evaluate_readiness_confirmation_eligibility,
    readiness_confirmation_eligibility_reasons
)
from usa_signal_bot.core.enums import ReadinessConfirmationDecision

def test_evaluate_readiness_confirmation_eligibility_queue():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": False,
        "zero_mutation_audit": {"status": "PASSED"}
    }
    decision = evaluate_readiness_confirmation_eligibility(payload)
    assert decision == ReadinessConfirmationDecision.QUEUE_FOR_HUMAN_REVIEW

def test_evaluate_readiness_confirmation_eligibility_missing():
    decision = evaluate_readiness_confirmation_eligibility({})
    assert decision == ReadinessConfirmationDecision.REQUEST_FIREWALL_AUDIT_REFRESH

def test_evaluate_readiness_confirmation_eligibility_block():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": True,
        "zero_mutation_audit": {"status": "PASSED"}
    }
    decision = evaluate_readiness_confirmation_eligibility(payload)
    assert decision == ReadinessConfirmationDecision.BLOCK
