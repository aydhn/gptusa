from usa_signal_bot.paper_readiness_confirmation.confirmation_decision import (
    determine_confirmation_decision,
    confirmation_decision_allows_activation
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle
from usa_signal_bot.core.enums import ActivationStillDeniedDecision, ReadinessConfirmationRiskFlag

def test_determine_confirmation_decision_queue_only():
    q = build_default_confirmation_queue_item()
    decision = determine_confirmation_decision(q)
    assert decision == ActivationStillDeniedDecision.REQUEST_MANUAL_REVIEW

def test_determine_confirmation_decision_with_bundle():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    decision = determine_confirmation_decision(q, b)
    assert decision == ActivationStillDeniedDecision.KEEP_ACTIVATION_DENIED_AND_QUEUE_HUMAN_REVIEW

def test_determine_confirmation_decision_block():
    q = build_default_confirmation_queue_item()
    q.safety_flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK)
    b = build_human_review_bundle(q)
    decision = determine_confirmation_decision(q, b)
    assert decision == ActivationStillDeniedDecision.BLOCK

def test_confirmation_decision_allows_activation():
    assert confirmation_decision_allows_activation(ActivationStillDeniedDecision.KEEP_ACTIVATION_DENIED_AND_QUEUE_HUMAN_REVIEW) is False
