import pytest
from pathlib import Path
from usa_signal_bot.paper_quarantine.quarantine_store import (
    quarantine_store_summary,
    write_quarantined_candidate_json,
    write_promotion_ticket_json,
    write_bridge_plan_json,
    write_paper_snapshot_ref_json,
    write_quarantine_audit_jsonl,
    write_quarantine_enrollment_review_json,
    read_quarantine_enrollment_review_json,
    get_latest_quarantine_enrollment_review,
)
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    PaperSnapshotRef,
    QuarantineAuditEntry,
    QuarantineEnrollmentReview,
)
from usa_signal_bot.core.enums import QuarantineCandidateStatus, PromotionTicketStatus, BridgePlanStatus, BridgeMode, QuarantineReportType, QuarantineEnrollmentDecision

def test_store_dirs(tmp_path):
    data_root = tmp_path / "data"
    s = quarantine_store_summary(data_root)
    assert "candidates" in s

def test_write_candidate(tmp_path):
    data_root = tmp_path / "data"
    c = QuarantinedPaperCandidate(candidate_id="c1", created_at_utc="", status=QuarantineCandidateStatus.ENROLLED, source_bundle_id=None, source_bundle_version=None, source_shadow_governance_review_id=None, source_shadow_decision=None, shadow_acceptance_score=None, risk_flags=[], policy=None, paper_snapshot_ref=None, promotion_ticket_id=None, bridge_plan_id=None, review_due_at_utc=None, allowed_for_active_paper=False, allowed_for_broker_execution=False, warnings=[], errors=[], metadata={})
    p = write_quarantined_candidate_json(data_root / "paper_quarantine" / "candidates" / "c1.json", c)
    assert p.exists()

def test_write_ticket(tmp_path):
    data_root = tmp_path / "data"
    t = ReadOnlyPromotionTicket(ticket_id="t1", created_at_utc="", status=PromotionTicketStatus.WAITING_REVIEW, candidate_id=None, source_bundle_id=None, source_bundle_version=None, source_shadow_governance_review_id=None, enrollment_decision=QuarantineEnrollmentDecision.UNKNOWN, title="", description="", evidence_refs=[], acceptance_score=None, risk_flags=[], required_followups=[], manual_review_required=True, manual_review_completed=False, read_only=True, allowed_for_active_paper=False, allowed_for_config_patch=False, allowed_for_broker_execution=False, warnings=[], errors=[], metadata={})
    p = write_promotion_ticket_json(data_root / "paper_quarantine" / "tickets" / "t1.json", t)
    assert p.exists()

def test_write_bridge_plan(tmp_path):
    data_root = tmp_path / "data"
    p = SupervisedDryRunBridgePlan(bridge_plan_id="b1", created_at_utc="", status=BridgePlanStatus.READY, mode=BridgeMode.SUPERVISED_DRY_RUN_PLANNING, candidate_id=None, ticket_id=None, paper_snapshot_ref_id=None, quarantine_output_path=None, allowed_operations=[], denied_operations=[], manual_review_required=True, bridge_execution_enabled=False, paper_state_mutation_enabled=False, paper_order_enabled=False, broker_order_enabled=False, telegram_real_send_enabled=False, production_config_write_enabled=False, safety_flags=[], warnings=[], errors=[], metadata={})
    path = write_bridge_plan_json(data_root / "paper_quarantine" / "bridge_plans" / "b1.json", p)
    assert path.exists()

def test_write_snapshot_ref(tmp_path):
    data_root = tmp_path / "data"
    ref = PaperSnapshotRef(snapshot_ref_id="r1", created_at_utc="", source="", snapshot_hash=None, snapshot_summary={}, read_only=True, allows_mutation=False, warnings=[], errors=[], metadata={})
    path = write_paper_snapshot_ref_json(data_root / "paper_quarantine" / "paper_snapshot_refs" / "r1.json", ref)
    assert path.exists()

def test_write_audit(tmp_path):
    data_root = tmp_path / "data"
    a = QuarantineAuditEntry(audit_id="a1", created_at_utc="", entity_type="", entity_id="", action="", decision=None, rationale="", evidence_refs=[], safety_flags=[], warnings=[], errors=[], metadata={})
    path = write_quarantine_audit_jsonl(data_root / "paper_quarantine" / "audit" / "a.jsonl", [a])
    assert path.exists()

def test_write_read_review(tmp_path):
    data_root = tmp_path / "data"
    r = QuarantineEnrollmentReview(review_id="r1", created_at_utc="", report_type=QuarantineReportType.ENROLLMENT_REVIEW, candidates=[], tickets=[], bridge_plans=[], audit_entries=[], output_paths={}, warnings=[], errors=[])
    path = write_quarantine_enrollment_review_json(data_root / "paper_quarantine" / "reviews" / "r1.json", r)
    assert path.exists()

    loaded = read_quarantine_enrollment_review_json(path)
    assert loaded["review_id"] == "r1"

    latest = get_latest_quarantine_enrollment_review(data_root)
    assert latest == path
