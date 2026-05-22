from usa_signal_bot.paper_readiness_confirmation.firewall_audit_adapter import (
    confirmation_queue_from_firewall_audit,
    attach_confirmation_metadata_to_firewall_audit_payload
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_report import build_readiness_confirmation_review
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle

def test_confirmation_queue_from_firewall_audit():
    payload = {"decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT", "activation_allowed": False}
    q = confirmation_queue_from_firewall_audit(payload)
    assert q.activation_denied_required is True

def test_attach_confirmation_metadata_to_firewall_audit_payload():
    payload = {"decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT", "activation_allowed": False}
    q = confirmation_queue_from_firewall_audit(payload)
    b = build_human_review_bundle(q)
    review = build_readiness_confirmation_review(q, b)

    res = attach_confirmation_metadata_to_firewall_audit_payload(payload, review)
    assert res["readiness_confirmation"]["review_id"] == review.review_id
