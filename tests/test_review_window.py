import pytest
import datetime
from usa_signal_bot.core.enums import QuarantineCandidateStatus
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate
from usa_signal_bot.paper_quarantine.review_window import (
    default_review_due_at,
    quarantine_review_expired,
    extend_review_window,
)

def test_default():
    due = default_review_due_at(7)
    assert due is not None

def test_expired():
    past = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).isoformat()
    assert quarantine_review_expired(past) is True

    future = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).isoformat()
    assert quarantine_review_expired(future) is False

def test_extend():
    c = QuarantinedPaperCandidate(candidate_id="c1", created_at_utc="", status=QuarantineCandidateStatus.ENROLLED, source_bundle_id=None, source_bundle_version=None, source_shadow_governance_review_id=None, source_shadow_decision=None, shadow_acceptance_score=None, risk_flags=[], policy=None, paper_snapshot_ref=None, promotion_ticket_id=None, bridge_plan_id=None, review_due_at_utc=None, allowed_for_active_paper=False, allowed_for_broker_execution=False, warnings=[], errors=[], metadata={})
    c = extend_review_window(c, 7)
    assert c.review_due_at_utc is not None
