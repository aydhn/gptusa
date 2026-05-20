import pytest
from usa_signal_bot.core.enums import PromotionTicketStatus
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate, ReadOnlyPromotionTicket
from usa_signal_bot.paper_quarantine.manual_review_gate import (
    manual_review_required_for_quarantine,
    manual_review_gate_status,
    build_manual_review_requirements,
    apply_manual_review_placeholder,
)

def test_required():
    c = QuarantinedPaperCandidate(candidate_id="c1", created_at_utc="", status=None, source_bundle_id=None, source_bundle_version=None, source_shadow_governance_review_id=None, source_shadow_decision=None, shadow_acceptance_score=None, risk_flags=[], policy=None, paper_snapshot_ref=None, promotion_ticket_id=None, bridge_plan_id=None, review_due_at_utc=None, allowed_for_active_paper=False, allowed_for_broker_execution=False, warnings=[], errors=[], metadata={})
    assert manual_review_required_for_quarantine(c, None) is True

def test_status():
    t = ReadOnlyPromotionTicket(ticket_id="t1", created_at_utc="", status=PromotionTicketStatus.WAITING_REVIEW, candidate_id=None, source_bundle_id=None, source_bundle_version=None, source_shadow_governance_review_id=None, enrollment_decision=None, title="", description="", evidence_refs=[], acceptance_score=None, risk_flags=[], required_followups=[], manual_review_required=True, manual_review_completed=False, read_only=True, allowed_for_active_paper=False, allowed_for_config_patch=False, allowed_for_broker_execution=False, warnings=[], errors=[], metadata={})
    assert manual_review_gate_status(t) == "WAITING_REVIEW"

def test_placeholder():
    t = ReadOnlyPromotionTicket(ticket_id="t1", created_at_utc="", status=PromotionTicketStatus.WAITING_REVIEW, candidate_id=None, source_bundle_id=None, source_bundle_version=None, source_shadow_governance_review_id=None, enrollment_decision=None, title="", description="", evidence_refs=[], acceptance_score=None, risk_flags=[], required_followups=[], manual_review_required=True, manual_review_completed=False, read_only=True, allowed_for_active_paper=False, allowed_for_config_patch=False, allowed_for_broker_execution=False, warnings=[], errors=[], metadata={})
    t = apply_manual_review_placeholder(t, True)
    assert t.manual_review_completed is True
