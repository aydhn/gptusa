import uuid
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    DryRunBridgeSessionStatus,
    DryRunBridgeMode,
    DryRunProposalType,
    DryRunProposalStatus,
    BridgeTelemetryEventType,
    HumanReviewCheckpointStatus,
    DryRunBridgeSafetyFlag,
    DryRunBridgeReportType
)

@dataclass
class DryRunBridgeContext:
    context_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    ticket_id: Optional[str]
    bridge_plan_id: Optional[str]
    paper_snapshot_ref_id: Optional[str]
    mode: DryRunBridgeMode
    read_only_paper_snapshot: dict[str, Any]
    candidate_metadata: dict[str, Any]
    quarantine_output_path: Optional[str]
    allow_paper_state_mutation: bool
    allow_paper_orders: bool
    allow_broker_orders: bool
    allow_telegram_real_send: bool
    allow_production_config_write: bool
    allow_active_paper_enable: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryRunProposal:
    proposal_id: str
    created_at_utc: str
    proposal_type: DryRunProposalType
    status: DryRunProposalStatus
    symbol: Optional[str]
    strategy_name: Optional[str]
    side: Optional[str]
    quantity: Optional[float]
    notional_usd: Optional[float]
    price: Optional[float]
    reason: str
    is_real_order: bool
    will_mutate_paper_state: bool
    will_send_to_broker: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BridgeTelemetryEvent:
    event_id: str
    created_at_utc: str
    event_type: BridgeTelemetryEventType
    session_id: Optional[str]
    ref_id: Optional[str]
    payload_summary: dict[str, Any]
    safety_flags: list[DryRunBridgeSafetyFlag]
    warnings: list[str]
    errors: list[str]

@dataclass
class HumanReviewCheckpoint:
    checkpoint_id: str
    created_at_utc: str
    session_id: Optional[str]
    candidate_id: Optional[str]
    ticket_id: Optional[str]
    status: HumanReviewCheckpointStatus
    required: bool
    reviewer_notes: Optional[str]
    reviewer_id: Optional[str]
    reviewed_at_utc: Optional[str]
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_config_patch: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryRunBridgeSession:
    session_id: str
    created_at_utc: str
    status: DryRunBridgeSessionStatus
    context: Optional[DryRunBridgeContext]
    proposals: list[DryRunProposal]
    telemetry_events: list[BridgeTelemetryEvent]
    human_checkpoints: list[HumanReviewCheckpoint]
    safety_flags: list[DryRunBridgeSafetyFlag]
    started_at_utc: Optional[str]
    completed_at_utc: Optional[str]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryRunBridgeReview:
    review_id: str
    created_at_utc: str
    report_type: DryRunBridgeReportType
    sessions: list[DryRunBridgeSession]
    telemetry_events: list[BridgeTelemetryEvent]
    checkpoints: list[HumanReviewCheckpoint]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def create_dry_run_bridge_context_id(prefix: str = "dry_run_context") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_run_proposal_id(prefix: str = "dry_run_proposal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bridge_telemetry_event_id(prefix: str = "bridge_telemetry") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_human_review_checkpoint_id(prefix: str = "human_checkpoint") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_run_bridge_session_id(prefix: str = "dry_run_bridge_session") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_run_bridge_review_id(prefix: str = "dry_run_bridge_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def dry_run_bridge_context_to_dict(item: DryRunBridgeContext) -> dict:
    return {
        "context_id": item.context_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "ticket_id": item.ticket_id,
        "bridge_plan_id": item.bridge_plan_id,
        "paper_snapshot_ref_id": item.paper_snapshot_ref_id,
        "mode": item.mode.value,
        "read_only_paper_snapshot": item.read_only_paper_snapshot,
        "candidate_metadata": item.candidate_metadata,
        "quarantine_output_path": item.quarantine_output_path,
        "allow_paper_state_mutation": item.allow_paper_state_mutation,
        "allow_paper_orders": item.allow_paper_orders,
        "allow_broker_orders": item.allow_broker_orders,
        "allow_telegram_real_send": item.allow_telegram_real_send,
        "allow_production_config_write": item.allow_production_config_write,
        "allow_active_paper_enable": item.allow_active_paper_enable,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_run_proposal_to_dict(item: DryRunProposal) -> dict:
    return {
        "proposal_id": item.proposal_id,
        "created_at_utc": item.created_at_utc,
        "proposal_type": item.proposal_type.value,
        "status": item.status.value,
        "symbol": item.symbol,
        "strategy_name": item.strategy_name,
        "side": item.side,
        "quantity": item.quantity,
        "notional_usd": item.notional_usd,
        "price": item.price,
        "reason": item.reason,
        "is_real_order": item.is_real_order,
        "will_mutate_paper_state": item.will_mutate_paper_state,
        "will_send_to_broker": item.will_send_to_broker,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def bridge_telemetry_event_to_dict(item: BridgeTelemetryEvent) -> dict:
    return {
        "event_id": item.event_id,
        "created_at_utc": item.created_at_utc,
        "event_type": item.event_type.value,
        "session_id": item.session_id,
        "ref_id": item.ref_id,
        "payload_summary": item.payload_summary,
        "safety_flags": [f.value for f in item.safety_flags],
        "warnings": item.warnings,
        "errors": item.errors,
    }

def human_review_checkpoint_to_dict(item: HumanReviewCheckpoint) -> dict:
    return {
        "checkpoint_id": item.checkpoint_id,
        "created_at_utc": item.created_at_utc,
        "session_id": item.session_id,
        "candidate_id": item.candidate_id,
        "ticket_id": item.ticket_id,
        "status": item.status.value,
        "required": item.required,
        "reviewer_notes": item.reviewer_notes,
        "reviewer_id": item.reviewer_id,
        "reviewed_at_utc": item.reviewed_at_utc,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_config_patch": item.allows_config_patch,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_run_bridge_session_to_dict(item: DryRunBridgeSession) -> dict:
    return {
        "session_id": item.session_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "context": dry_run_bridge_context_to_dict(item.context) if item.context else None,
        "proposals": [dry_run_proposal_to_dict(p) for p in item.proposals],
        "telemetry_events": [bridge_telemetry_event_to_dict(e) for e in item.telemetry_events],
        "human_checkpoints": [human_review_checkpoint_to_dict(c) for c in item.human_checkpoints],
        "safety_flags": [f.value for f in item.safety_flags],
        "started_at_utc": item.started_at_utc,
        "completed_at_utc": item.completed_at_utc,
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_run_bridge_review_to_dict(item: DryRunBridgeReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "sessions": [dry_run_bridge_session_to_dict(s) for s in item.sessions],
        "telemetry_events": [bridge_telemetry_event_to_dict(e) for e in item.telemetry_events],
        "checkpoints": [human_review_checkpoint_to_dict(c) for c in item.checkpoints],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_dry_run_bridge_context(item: DryRunBridgeContext) -> None:
    if item.allow_paper_state_mutation:
        raise ValueError("DryRunBridgeContext allows paper state mutation. This is strictly forbidden.")
    if item.allow_paper_orders:
        raise ValueError("DryRunBridgeContext allows paper orders. This is strictly forbidden.")
    if item.allow_broker_orders:
        raise ValueError("DryRunBridgeContext allows broker orders. This is strictly forbidden.")
    if item.allow_telegram_real_send:
        raise ValueError("DryRunBridgeContext allows real Telegram send. This is strictly forbidden.")
    if item.allow_production_config_write:
        raise ValueError("DryRunBridgeContext allows production config write. This is strictly forbidden.")
    if item.allow_active_paper_enable:
        raise ValueError("DryRunBridgeContext allows active paper enable. This is strictly forbidden.")

def validate_dry_run_proposal(item: DryRunProposal) -> None:
    if item.is_real_order:
        raise ValueError("DryRunProposal is marked as real order. This is strictly forbidden.")
    if item.will_mutate_paper_state:
        raise ValueError("DryRunProposal will mutate paper state. This is strictly forbidden.")
    if item.will_send_to_broker:
        raise ValueError("DryRunProposal will send to broker. This is strictly forbidden.")

def validate_human_review_checkpoint(item: HumanReviewCheckpoint) -> None:
    if item.allows_active_paper:
        raise ValueError("HumanReviewCheckpoint allows active paper. This is strictly forbidden.")
    if item.allows_broker_execution:
        raise ValueError("HumanReviewCheckpoint allows broker execution. This is strictly forbidden.")
    if item.allows_config_patch:
        raise ValueError("HumanReviewCheckpoint allows config patch. This is strictly forbidden.")

def validate_dry_run_bridge_session(item: DryRunBridgeSession) -> None:
    if item.context:
        validate_dry_run_bridge_context(item.context)
    for proposal in item.proposals:
        validate_dry_run_proposal(proposal)
    for checkpoint in item.human_checkpoints:
        validate_human_review_checkpoint(checkpoint)

def validate_dry_run_bridge_review(item: DryRunBridgeReview) -> None:
    for session in item.sessions:
        validate_dry_run_bridge_session(session)
    for checkpoint in item.checkpoints:
        validate_human_review_checkpoint(checkpoint)
