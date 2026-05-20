import pytest
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate, ReadOnlyPromotionTicket, SupervisedDryRunBridgePlan
from usa_signal_bot.core.enums import QuarantineCandidateStatus
from usa_signal_bot.paper_quarantine.enrollment_report import (
    build_quarantine_enrollment_review,
    quarantine_limitations_text,
)

def test_build(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.risk_flags = []
    c.allowed_for_active_paper = False
    c.allowed_for_broker_execution = False
    c.review_due_at_utc = None
    c.candidate_id = "c1"
    c.status = QuarantineCandidateStatus.ENROLLED
    c.source_bundle_id = "b1"
    c.source_bundle_version = "v1"
    c.source_shadow_governance_review_id = "r1"
    c.source_shadow_decision = "ACCEPT"
    c.shadow_acceptance_score = 80.0
    c.policy = None
    c.paper_snapshot_ref = None
    c.promotion_ticket_id = None
    c.bridge_plan_id = None
    c.warnings = []
    c.errors = []
    c.metadata = {}

    r = build_quarantine_enrollment_review(c, None, None)
    assert r.candidates[0].candidate_id == c.candidate_id

def test_limitations():
    t = quarantine_limitations_text()
    assert "No broker / live / demo order execution" in t
