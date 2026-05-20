from dataclasses import dataclass, field
from typing import Any
import uuid

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

@dataclass
class QuarantinePolicy:
    policy_id: str
    created_at_utc: str
    require_manual_review: bool
    require_shadow_governance_acceptance: bool
    min_shadow_acceptance_score: float
    allow_paper_state_mutation: bool
    allow_paper_orders: bool
    allow_broker_orders: bool
    allow_telegram_real_send: bool
    allow_production_config_write: bool
    allowed_bridge_operations: list[BridgeOperation]
    denied_bridge_operations: list[BridgeOperation]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSnapshotRef:
    snapshot_ref_id: str
    created_at_utc: str
    source: str
    snapshot_hash: str | None
    snapshot_summary: dict[str, Any]
    read_only: bool
    allows_mutation: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class QuarantinedPaperCandidate:
    candidate_id: str
    created_at_utc: str
    status: QuarantineCandidateStatus
    source_bundle_id: str | None
    source_bundle_version: str | None
    source_shadow_governance_review_id: str | None
    source_shadow_decision: str | None
    shadow_acceptance_score: float | None
    risk_flags: list[QuarantineSafetyFlag]
    policy: QuarantinePolicy | None
    paper_snapshot_ref: PaperSnapshotRef | None
    promotion_ticket_id: str | None
    bridge_plan_id: str | None
    review_due_at_utc: str | None
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadOnlyPromotionTicket:
    ticket_id: str
    created_at_utc: str
    status: PromotionTicketStatus
    candidate_id: str | None
    source_bundle_id: str | None
    source_bundle_version: str | None
    source_shadow_governance_review_id: str | None
    enrollment_decision: QuarantineEnrollmentDecision
    title: str
    description: str
    evidence_refs: list[str]
    acceptance_score: float | None
    risk_flags: list[QuarantineSafetyFlag]
    required_followups: list[str]
    manual_review_required: bool
    manual_review_completed: bool
    read_only: bool
    allowed_for_active_paper: bool
    allowed_for_config_patch: bool
    allowed_for_broker_execution: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SupervisedDryRunBridgePlan:
    bridge_plan_id: str
    created_at_utc: str
    status: BridgePlanStatus
    mode: BridgeMode
    candidate_id: str | None
    ticket_id: str | None
    paper_snapshot_ref_id: str | None
    quarantine_output_path: str | None
    allowed_operations: list[BridgeOperation]
    denied_operations: list[BridgeOperation]
    manual_review_required: bool
    bridge_execution_enabled: bool
    paper_state_mutation_enabled: bool
    paper_order_enabled: bool
    broker_order_enabled: bool
    telegram_real_send_enabled: bool
    production_config_write_enabled: bool
    safety_flags: list[QuarantineSafetyFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class QuarantineAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: str | None
    rationale: str
    evidence_refs: list[str]
    safety_flags: list[QuarantineSafetyFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class QuarantineEnrollmentReview:
    review_id: str
    created_at_utc: str
    report_type: QuarantineReportType
    candidates: list[QuarantinedPaperCandidate]
    tickets: list[ReadOnlyPromotionTicket]
    bridge_plans: list[SupervisedDryRunBridgePlan]
    audit_entries: list[QuarantineAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def quarantine_policy_to_dict(item: QuarantinePolicy) -> dict:
    return {
        "policy_id": item.policy_id,
        "created_at_utc": item.created_at_utc,
        "require_manual_review": item.require_manual_review,
        "require_shadow_governance_acceptance": item.require_shadow_governance_acceptance,
        "min_shadow_acceptance_score": item.min_shadow_acceptance_score,
        "allow_paper_state_mutation": item.allow_paper_state_mutation,
        "allow_paper_orders": item.allow_paper_orders,
        "allow_broker_orders": item.allow_broker_orders,
        "allow_telegram_real_send": item.allow_telegram_real_send,
        "allow_production_config_write": item.allow_production_config_write,
        "allowed_bridge_operations": [op.value for op in item.allowed_bridge_operations],
        "denied_bridge_operations": [op.value for op in item.denied_bridge_operations],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def paper_snapshot_ref_to_dict(item: PaperSnapshotRef) -> dict:
    return {
        "snapshot_ref_id": item.snapshot_ref_id,
        "created_at_utc": item.created_at_utc,
        "source": item.source,
        "snapshot_hash": item.snapshot_hash,
        "snapshot_summary": item.snapshot_summary,
        "read_only": item.read_only,
        "allows_mutation": item.allows_mutation,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def quarantined_paper_candidate_to_dict(item: QuarantinedPaperCandidate) -> dict:
    return {
        "candidate_id": item.candidate_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "source_bundle_id": item.source_bundle_id,
        "source_bundle_version": item.source_bundle_version,
        "source_shadow_governance_review_id": item.source_shadow_governance_review_id,
        "source_shadow_decision": item.source_shadow_decision,
        "shadow_acceptance_score": item.shadow_acceptance_score,
        "risk_flags": [f.value for f in item.risk_flags],
        "policy": quarantine_policy_to_dict(item.policy) if item.policy else None,
        "paper_snapshot_ref": paper_snapshot_ref_to_dict(item.paper_snapshot_ref) if item.paper_snapshot_ref else None,
        "promotion_ticket_id": item.promotion_ticket_id,
        "bridge_plan_id": item.bridge_plan_id,
        "review_due_at_utc": item.review_due_at_utc,
        "allowed_for_active_paper": item.allowed_for_active_paper,
        "allowed_for_broker_execution": item.allowed_for_broker_execution,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def read_only_promotion_ticket_to_dict(item: ReadOnlyPromotionTicket) -> dict:
    return {
        "ticket_id": item.ticket_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "candidate_id": item.candidate_id,
        "source_bundle_id": item.source_bundle_id,
        "source_bundle_version": item.source_bundle_version,
        "source_shadow_governance_review_id": item.source_shadow_governance_review_id,
        "enrollment_decision": item.enrollment_decision.value,
        "title": item.title,
        "description": item.description,
        "evidence_refs": item.evidence_refs,
        "acceptance_score": item.acceptance_score,
        "risk_flags": [f.value for f in item.risk_flags],
        "required_followups": item.required_followups,
        "manual_review_required": item.manual_review_required,
        "manual_review_completed": item.manual_review_completed,
        "read_only": item.read_only,
        "allowed_for_active_paper": item.allowed_for_active_paper,
        "allowed_for_config_patch": item.allowed_for_config_patch,
        "allowed_for_broker_execution": item.allowed_for_broker_execution,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def supervised_dry_run_bridge_plan_to_dict(item: SupervisedDryRunBridgePlan) -> dict:
    return {
        "bridge_plan_id": item.bridge_plan_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "mode": item.mode.value,
        "candidate_id": item.candidate_id,
        "ticket_id": item.ticket_id,
        "paper_snapshot_ref_id": item.paper_snapshot_ref_id,
        "quarantine_output_path": item.quarantine_output_path,
        "allowed_operations": [op.value for op in item.allowed_operations],
        "denied_operations": [op.value for op in item.denied_operations],
        "manual_review_required": item.manual_review_required,
        "bridge_execution_enabled": item.bridge_execution_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "paper_order_enabled": item.paper_order_enabled,
        "broker_order_enabled": item.broker_order_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "production_config_write_enabled": item.production_config_write_enabled,
        "safety_flags": [f.value for f in item.safety_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def quarantine_audit_entry_to_dict(item: QuarantineAuditEntry) -> dict:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "action": item.action,
        "decision": item.decision,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "safety_flags": [f.value for f in item.safety_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def quarantine_enrollment_review_to_dict(item: QuarantineEnrollmentReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "candidates": [quarantined_paper_candidate_to_dict(c) for c in item.candidates],
        "tickets": [read_only_promotion_ticket_to_dict(t) for t in item.tickets],
        "bridge_plans": [supervised_dry_run_bridge_plan_to_dict(p) for p in item.bridge_plans],
        "audit_entries": [quarantine_audit_entry_to_dict(a) for a in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

from usa_signal_bot.core.exceptions import QuarantineValidationError

def validate_quarantine_policy(item: QuarantinePolicy) -> None:
    if item.allow_paper_state_mutation:
        raise QuarantineValidationError("QuarantinePolicy allow_paper_state_mutation must be False")
    if item.allow_paper_orders:
        raise QuarantineValidationError("QuarantinePolicy allow_paper_orders must be False")
    if item.allow_broker_orders:
        raise QuarantineValidationError("QuarantinePolicy allow_broker_orders must be False")
    if item.allow_telegram_real_send:
        raise QuarantineValidationError("QuarantinePolicy allow_telegram_real_send must be False")
    if item.allow_production_config_write:
        raise QuarantineValidationError("QuarantinePolicy allow_production_config_write must be False")

    denied = set(item.denied_operations) if hasattr(item, "denied_operations") else set(item.denied_bridge_operations)
    allowed = set(item.allowed_operations) if hasattr(item, "allowed_operations") else set(item.allowed_bridge_operations)

    forbidden = [
        BridgeOperation.WRITE_PAPER_STATE,
        BridgeOperation.SEND_PAPER_ORDER,
        BridgeOperation.SEND_BROKER_ORDER,
        BridgeOperation.SEND_TELEGRAM_REAL,
        BridgeOperation.WRITE_PRODUCTION_CONFIG,
    ]

    for op in forbidden:
        if op in allowed:
            raise QuarantineValidationError(f"BridgeOperation {op.value} cannot be in allowed operations")

def validate_paper_snapshot_ref(item: PaperSnapshotRef) -> None:
    if not item.read_only:
        raise QuarantineValidationError("PaperSnapshotRef read_only must be True")
    if item.allows_mutation:
        raise QuarantineValidationError("PaperSnapshotRef allows_mutation must be False")

def validate_quarantined_paper_candidate(item: QuarantinedPaperCandidate) -> None:
    if item.allowed_for_active_paper:
        raise QuarantineValidationError("QuarantinedPaperCandidate allowed_for_active_paper must be False")
    if item.allowed_for_broker_execution:
        raise QuarantineValidationError("QuarantinedPaperCandidate allowed_for_broker_execution must be False")

def validate_read_only_promotion_ticket(item: ReadOnlyPromotionTicket) -> None:
    if not item.read_only:
        raise QuarantineValidationError("ReadOnlyPromotionTicket read_only must be True")
    if item.allowed_for_active_paper:
        raise QuarantineValidationError("ReadOnlyPromotionTicket allowed_for_active_paper must be False")
    if item.allowed_for_config_patch:
        raise QuarantineValidationError("ReadOnlyPromotionTicket allowed_for_config_patch must be False")
    if item.allowed_for_broker_execution:
        raise QuarantineValidationError("ReadOnlyPromotionTicket allowed_for_broker_execution must be False")

def validate_supervised_dry_run_bridge_plan(item: SupervisedDryRunBridgePlan) -> None:
    if item.bridge_execution_enabled:
        raise QuarantineValidationError("SupervisedDryRunBridgePlan bridge_execution_enabled must be False")
    if item.paper_state_mutation_enabled:
        raise QuarantineValidationError("SupervisedDryRunBridgePlan paper_state_mutation_enabled must be False")
    if item.paper_order_enabled:
        raise QuarantineValidationError("SupervisedDryRunBridgePlan paper_order_enabled must be False")
    if item.broker_order_enabled:
        raise QuarantineValidationError("SupervisedDryRunBridgePlan broker_order_enabled must be False")
    if item.telegram_real_send_enabled:
        raise QuarantineValidationError("SupervisedDryRunBridgePlan telegram_real_send_enabled must be False")
    if item.production_config_write_enabled:
        raise QuarantineValidationError("SupervisedDryRunBridgePlan production_config_write_enabled must be False")

    allowed = set(item.allowed_operations)
    forbidden = [
        BridgeOperation.WRITE_PAPER_STATE,
        BridgeOperation.SEND_PAPER_ORDER,
        BridgeOperation.SEND_BROKER_ORDER,
        BridgeOperation.SEND_TELEGRAM_REAL,
        BridgeOperation.WRITE_PRODUCTION_CONFIG,
    ]

    for op in forbidden:
        if op in allowed:
            raise QuarantineValidationError(f"BridgeOperation {op.value} cannot be in allowed operations")

def validate_quarantine_enrollment_review(item: QuarantineEnrollmentReview) -> None:
    for c in item.candidates:
        validate_quarantined_paper_candidate(c)
    for t in item.tickets:
        validate_read_only_promotion_ticket(t)
    for p in item.bridge_plans:
        validate_supervised_dry_run_bridge_plan(p)

def create_quarantine_policy_id(prefix: str = "quarantine_policy") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_snapshot_ref_id(prefix: str = "paper_snapshot_ref") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_quarantined_candidate_id(prefix: str = "quarantined_candidate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_promotion_ticket_id(prefix: str = "promotion_ticket") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bridge_plan_id(prefix: str = "dry_run_bridge") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_quarantine_audit_id(prefix: str = "quarantine_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_quarantine_review_id(prefix: str = "quarantine_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
