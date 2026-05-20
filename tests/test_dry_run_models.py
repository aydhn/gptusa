import pytest
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal,
    BridgeTelemetryEvent,
    HumanReviewCheckpoint,
    DryRunBridgeSession,
    DryRunBridgeReview,
    DryRunBridgeMode,
    DryRunProposalType,
    DryRunProposalStatus,
    BridgeTelemetryEventType,
    HumanReviewCheckpointStatus,
    DryRunBridgeReportType,
    create_dry_run_bridge_context_id,
    create_dry_run_proposal_id,
    create_bridge_telemetry_event_id,
    create_human_review_checkpoint_id,
    validate_dry_run_bridge_context,
    validate_dry_run_proposal,
    validate_human_review_checkpoint,
    validate_dry_run_bridge_session,
    validate_dry_run_bridge_review,
    dry_run_bridge_context_to_dict,
    dry_run_bridge_review_to_dict
)

def test_dry_run_bridge_context_valid():
    ctx = DryRunBridgeContext(
        context_id=create_dry_run_bridge_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id="cand_1",
        ticket_id="ticket_1",
        bridge_plan_id="plan_1",
        paper_snapshot_ref_id="snap_1",
        mode=DryRunBridgeMode.FULL_SUPERVISED_DRY_RUN,
        read_only_paper_snapshot={},
        candidate_metadata={},
        quarantine_output_path="/tmp/output",
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allow_active_paper_enable=False,
        warnings=[],
        errors=[]
    )
    validate_dry_run_bridge_context(ctx)

def test_dry_run_bridge_context_invalid():
    ctx = DryRunBridgeContext(
        context_id=create_dry_run_bridge_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id="cand_1",
        ticket_id="ticket_1",
        bridge_plan_id="plan_1",
        paper_snapshot_ref_id="snap_1",
        mode=DryRunBridgeMode.FULL_SUPERVISED_DRY_RUN,
        read_only_paper_snapshot={},
        candidate_metadata={},
        quarantine_output_path="/tmp/output",
        allow_paper_state_mutation=False,
        allow_paper_orders=True, # Invalid
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allow_active_paper_enable=False,
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError):
        validate_dry_run_bridge_context(ctx)

def test_dry_run_proposal_valid():
    prop = DryRunProposal(
        proposal_id=create_dry_run_proposal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        proposal_type=DryRunProposalType.SIGNAL_PROPOSAL,
        status=DryRunProposalStatus.CREATED,
        symbol="SPY",
        strategy_name="strat_1",
        side="BUY",
        quantity=1.0,
        notional_usd=100.0,
        price=100.0,
        reason="Test",
        is_real_order=False,
        will_mutate_paper_state=False,
        will_send_to_broker=False,
        warnings=[],
        errors=[]
    )
    validate_dry_run_proposal(prop)

def test_dry_run_proposal_invalid():
    prop = DryRunProposal(
        proposal_id=create_dry_run_proposal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        proposal_type=DryRunProposalType.SIGNAL_PROPOSAL,
        status=DryRunProposalStatus.CREATED,
        symbol="SPY",
        strategy_name="strat_1",
        side="BUY",
        quantity=1.0,
        notional_usd=100.0,
        price=100.0,
        reason="Test",
        is_real_order=True, # Invalid
        will_mutate_paper_state=False,
        will_send_to_broker=False,
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError):
        validate_dry_run_proposal(prop)

def test_human_review_checkpoint_valid():
    chk = HumanReviewCheckpoint(
        checkpoint_id=create_human_review_checkpoint_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        session_id="session_1",
        candidate_id="cand_1",
        ticket_id="ticket_1",
        status=HumanReviewCheckpointStatus.REQUIRED,
        required=True,
        reviewer_notes=None,
        reviewer_id=None,
        reviewed_at_utc=None,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    validate_human_review_checkpoint(chk)

def test_human_review_checkpoint_invalid():
    chk = HumanReviewCheckpoint(
        checkpoint_id=create_human_review_checkpoint_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        session_id="session_1",
        candidate_id="cand_1",
        ticket_id="ticket_1",
        status=HumanReviewCheckpointStatus.REQUIRED,
        required=True,
        reviewer_notes=None,
        reviewer_id=None,
        reviewed_at_utc=None,
        allows_active_paper=True, # Invalid
        allows_broker_execution=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError):
        validate_human_review_checkpoint(chk)

def test_serialize():
    ctx = DryRunBridgeContext(
        context_id=create_dry_run_bridge_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id="cand_1",
        ticket_id="ticket_1",
        bridge_plan_id="plan_1",
        paper_snapshot_ref_id="snap_1",
        mode=DryRunBridgeMode.FULL_SUPERVISED_DRY_RUN,
        read_only_paper_snapshot={},
        candidate_metadata={},
        quarantine_output_path="/tmp/output",
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allow_active_paper_enable=False,
        warnings=[],
        errors=[]
    )
    d = dry_run_bridge_context_to_dict(ctx)
    assert d["context_id"] == ctx.context_id
