import pytest
import datetime
from usa_signal_bot.core.enums import (
    QuarantineCandidateStatus,
    QuarantineEnrollmentDecision,
    PromotionTicketStatus,
    BridgePlanStatus,
    BridgeMode,
    BridgeOperation,
    QuarantineSafetyFlag,
    QuarantineReportType,
)
from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinePolicy,
    PaperSnapshotRef,
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    QuarantineAuditEntry,
    QuarantineEnrollmentReview,
    create_quarantine_policy_id,
    create_paper_snapshot_ref_id,
    create_quarantined_candidate_id,
    create_promotion_ticket_id,
    create_bridge_plan_id,
    create_quarantine_audit_id,
    create_quarantine_review_id,
    validate_quarantine_policy,
    validate_paper_snapshot_ref,
    validate_quarantined_paper_candidate,
    validate_read_only_promotion_ticket,
    validate_supervised_dry_run_bridge_plan,
    validate_quarantine_enrollment_review,
)
from usa_signal_bot.core.exceptions import QuarantineValidationError

def test_quarantine_policy_valid():
    policy = QuarantinePolicy(
        policy_id="p1",
        created_at_utc="2024-01-01T00:00:00Z",
        require_manual_review=True,
        require_shadow_governance_acceptance=True,
        min_shadow_acceptance_score=70.0,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allowed_bridge_operations=[BridgeOperation.READ_PROMOTION_TICKET],
        denied_bridge_operations=[BridgeOperation.WRITE_PAPER_STATE],
        warnings=[],
        errors=[]
    )
    validate_quarantine_policy(policy)

def test_paper_snapshot_ref_valid():
    ref = PaperSnapshotRef(
        snapshot_ref_id="r1",
        created_at_utc="2024-01-01T00:00:00Z",
        source="test",
        snapshot_hash="hash",
        snapshot_summary={},
        read_only=True,
        allows_mutation=False,
        warnings=[],
        errors=[]
    )
    validate_paper_snapshot_ref(ref)

def test_quarantined_paper_candidate_valid():
    c = QuarantinedPaperCandidate(
        candidate_id="c1",
        created_at_utc="2024-01-01T00:00:00Z",
        status=QuarantineCandidateStatus.ENROLLED,
        source_bundle_id="b1",
        source_bundle_version="v1",
        source_shadow_governance_review_id="sr1",
        source_shadow_decision="ACCEPT",
        shadow_acceptance_score=80.0,
        risk_flags=[],
        policy=None,
        paper_snapshot_ref=None,
        promotion_ticket_id=None,
        bridge_plan_id=None,
        review_due_at_utc=None,
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )
    validate_quarantined_paper_candidate(c)

def test_read_only_promotion_ticket_valid():
    t = ReadOnlyPromotionTicket(
        ticket_id="t1",
        created_at_utc="2024-01-01T00:00:00Z",
        status=PromotionTicketStatus.READ_ONLY_CREATED,
        candidate_id="c1",
        source_bundle_id="b1",
        source_bundle_version="v1",
        source_shadow_governance_review_id="sr1",
        enrollment_decision=QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE,
        title="t",
        description="d",
        evidence_refs=[],
        acceptance_score=80.0,
        risk_flags=[],
        required_followups=[],
        manual_review_required=True,
        manual_review_completed=False,
        read_only=True,
        allowed_for_active_paper=False,
        allowed_for_config_patch=False,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )
    validate_read_only_promotion_ticket(t)

def test_supervised_dry_run_bridge_plan_valid():
    p = SupervisedDryRunBridgePlan(
        bridge_plan_id="p1",
        created_at_utc="2024-01-01T00:00:00Z",
        status=BridgePlanStatus.READY,
        mode=BridgeMode.SUPERVISED_DRY_RUN_PLANNING,
        candidate_id="c1",
        ticket_id="t1",
        paper_snapshot_ref_id="r1",
        quarantine_output_path="path",
        allowed_operations=[BridgeOperation.READ_PROMOTION_TICKET],
        denied_operations=[BridgeOperation.WRITE_PAPER_STATE],
        manual_review_required=True,
        bridge_execution_enabled=False,
        paper_state_mutation_enabled=False,
        paper_order_enabled=False,
        broker_order_enabled=False,
        telegram_real_send_enabled=False,
        production_config_write_enabled=False,
        safety_flags=[],
        warnings=[],
        errors=[]
    )
    validate_supervised_dry_run_bridge_plan(p)

def test_invalid_active_paper():
    c = QuarantinedPaperCandidate(
        candidate_id="c1",
        created_at_utc="2024-01-01T00:00:00Z",
        status=QuarantineCandidateStatus.ENROLLED,
        source_bundle_id="b1",
        source_bundle_version="v1",
        source_shadow_governance_review_id="sr1",
        source_shadow_decision="ACCEPT",
        shadow_acceptance_score=80.0,
        risk_flags=[],
        policy=None,
        paper_snapshot_ref=None,
        promotion_ticket_id=None,
        bridge_plan_id=None,
        review_due_at_utc=None,
        allowed_for_active_paper=True,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )
    with pytest.raises(QuarantineValidationError):
        validate_quarantined_paper_candidate(c)

def test_invalid_read_only():
    t = ReadOnlyPromotionTicket(
        ticket_id="t1",
        created_at_utc="2024-01-01T00:00:00Z",
        status=PromotionTicketStatus.READ_ONLY_CREATED,
        candidate_id="c1",
        source_bundle_id="b1",
        source_bundle_version="v1",
        source_shadow_governance_review_id="sr1",
        enrollment_decision=QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE,
        title="t",
        description="d",
        evidence_refs=[],
        acceptance_score=80.0,
        risk_flags=[],
        required_followups=[],
        manual_review_required=True,
        manual_review_completed=False,
        read_only=False,
        allowed_for_active_paper=False,
        allowed_for_config_patch=False,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )
    with pytest.raises(QuarantineValidationError):
        validate_read_only_promotion_ticket(t)

def test_invalid_mutation_enabled():
    p = SupervisedDryRunBridgePlan(
        bridge_plan_id="p1",
        created_at_utc="2024-01-01T00:00:00Z",
        status=BridgePlanStatus.READY,
        mode=BridgeMode.SUPERVISED_DRY_RUN_PLANNING,
        candidate_id="c1",
        ticket_id="t1",
        paper_snapshot_ref_id="r1",
        quarantine_output_path="path",
        allowed_operations=[BridgeOperation.READ_PROMOTION_TICKET],
        denied_operations=[BridgeOperation.WRITE_PAPER_STATE],
        manual_review_required=True,
        bridge_execution_enabled=False,
        paper_state_mutation_enabled=True,
        paper_order_enabled=False,
        broker_order_enabled=False,
        telegram_real_send_enabled=False,
        production_config_write_enabled=False,
        safety_flags=[],
        warnings=[],
        errors=[]
    )
    with pytest.raises(QuarantineValidationError):
        validate_supervised_dry_run_bridge_plan(p)
