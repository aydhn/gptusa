import pytest
from usa_signal_bot.core.enums import QuarantineEnrollmentDecision, PromotionTicketStatus
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate
from usa_signal_bot.paper_quarantine.promotion_ticket import (
    build_promotion_ticket_for_candidate,
    build_ticket_from_shadow_governance_payload,
    promotion_ticket_to_text,
)

def test_build_ticket(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.candidate_id = "c1"
    c.source_bundle_id = "b1"
    c.source_bundle_version = "v1"
    c.source_shadow_governance_review_id = "r1"
    c.shadow_acceptance_score = 80.0
    c.risk_flags = []

    t = build_promotion_ticket_for_candidate(c, QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE)
    assert t.read_only is True
    assert t.allowed_for_active_paper is False
    assert t.allowed_for_config_patch is False
    assert t.allowed_for_broker_execution is False

def test_build_from_payload():
    t = build_ticket_from_shadow_governance_payload({"decision": "ACCEPT", "score": 80.0})
    assert t.read_only is True

def test_to_text(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.candidate_id = "c1"
    c.source_bundle_id = "b1"
    c.source_bundle_version = "v1"
    c.source_shadow_governance_review_id = "r1"
    c.shadow_acceptance_score = 80.0
    c.risk_flags = []
    t = build_promotion_ticket_for_candidate(c, QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE)
    assert "Read Only: True" in promotion_ticket_to_text(t)
