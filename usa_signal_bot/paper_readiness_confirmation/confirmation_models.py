from dataclasses import dataclass, field
from typing import Any
import datetime
from uuid import uuid4

from usa_signal_bot.core.enums import (
    ReadinessConfirmationQueueStatus,
    ReadinessConfirmationDecision,
    HumanReviewBundleStatus,
    ReviewChecklistItemStatus,
    ActivationStillDeniedRegistryStatus,
    ActivationStillDeniedDecision,
    ReadinessConfirmationRiskFlag,
    ReadinessConfidenceLevel,
    ReadinessConfirmationReportType
)

@dataclass
class ReadinessConfirmationQueueItem:
    queue_item_id: str
    created_at_utc: str
    status: ReadinessConfirmationQueueStatus
    decision: ReadinessConfirmationDecision
    candidate_id: str | None
    source_firewall_audit_review_id: str | None
    source_readiness_audit_checkpoint_id: str | None
    source_zero_mutation_audit_id: str | None
    source_firewall_replay_result_id: str | None
    evidence_refs: list[str]
    required_followups: list[str]
    readiness_confidence: ReadinessConfidenceLevel
    safety_flags: list[ReadinessConfirmationRiskFlag]
    manual_review_required: bool
    activation_denied_required: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class HumanReviewBundle:
    bundle_id: str
    created_at_utc: str
    status: HumanReviewBundleStatus
    candidate_id: str | None
    queue_item_id: str | None
    title: str
    summary: dict[str, Any]
    checklist_refs: list[str]
    evidence_refs: list[str]
    reviewer_note_refs: list[str]
    required_reviewer_actions: list[str]
    safety_flags: list[ReadinessConfirmationRiskFlag]
    activation_denied: bool
    activation_allowed: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class HumanReviewChecklistItem:
    checklist_item_id: str
    created_at_utc: str
    category: str
    title: str
    status: ReviewChecklistItemStatus
    observed_value: Any | None
    expected_value: Any | None
    description: str
    required: bool
    risk_flags: list[ReadinessConfirmationRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReviewerNote:
    note_id: str
    created_at_utc: str
    reviewer_id: str | None
    candidate_id: str | None
    bundle_id: str | None
    note_text: str
    decision_hint: str | None
    requires_followup: bool
    followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ActivationStillDeniedRegistryEntry:
    registry_entry_id: str
    created_at_utc: str
    status: ActivationStillDeniedRegistryStatus
    decision: ActivationStillDeniedDecision
    candidate_id: str | None
    queue_item_id: str | None
    bundle_id: str | None
    source_checkpoint_id: str | None
    activation_denied: bool
    activation_allowed: bool
    denial_reason: str
    required_followups: list[str]
    safety_flags: list[ReadinessConfirmationRiskFlag]
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessConfirmationAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: str | None
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[ReadinessConfirmationRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessConfirmationReview:
    review_id: str
    created_at_utc: str
    report_type: ReadinessConfirmationReportType
    queue_items: list[ReadinessConfirmationQueueItem]
    bundles: list[HumanReviewBundle]
    checklist_items: list[HumanReviewChecklistItem]
    reviewer_notes: list[ReviewerNote]
    registry_entries: list[ActivationStillDeniedRegistryEntry]
    audit_entries: list[ReadinessConfirmationAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def readiness_confirmation_queue_item_to_dict(item: ReadinessConfirmationQueueItem) -> dict:
    return {
        "queue_item_id": item.queue_item_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "source_firewall_audit_review_id": item.source_firewall_audit_review_id,
        "source_readiness_audit_checkpoint_id": item.source_readiness_audit_checkpoint_id,
        "source_zero_mutation_audit_id": item.source_zero_mutation_audit_id,
        "source_firewall_replay_result_id": item.source_firewall_replay_result_id,
        "evidence_refs": item.evidence_refs,
        "required_followups": item.required_followups,
        "readiness_confidence": item.readiness_confidence.value,
        "safety_flags": [f.value for f in item.safety_flags],
        "manual_review_required": item.manual_review_required,
        "activation_denied_required": item.activation_denied_required,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def human_review_bundle_to_dict(item: HumanReviewBundle) -> dict:
    return {
        "bundle_id": item.bundle_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "candidate_id": item.candidate_id,
        "queue_item_id": item.queue_item_id,
        "title": item.title,
        "summary": item.summary,
        "checklist_refs": item.checklist_refs,
        "evidence_refs": item.evidence_refs,
        "reviewer_note_refs": item.reviewer_note_refs,
        "required_reviewer_actions": item.required_reviewer_actions,
        "safety_flags": [f.value for f in item.safety_flags],
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def human_review_checklist_item_to_dict(item: HumanReviewChecklistItem) -> dict:
    return {
        "checklist_item_id": item.checklist_item_id,
        "created_at_utc": item.created_at_utc,
        "category": item.category,
        "title": item.title,
        "status": item.status.value,
        "observed_value": item.observed_value,
        "expected_value": item.expected_value,
        "description": item.description,
        "required": item.required,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def reviewer_note_to_dict(item: ReviewerNote) -> dict:
    return {
        "note_id": item.note_id,
        "created_at_utc": item.created_at_utc,
        "reviewer_id": item.reviewer_id,
        "candidate_id": item.candidate_id,
        "bundle_id": item.bundle_id,
        "note_text": item.note_text,
        "decision_hint": item.decision_hint,
        "requires_followup": item.requires_followup,
        "followups": item.followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def activation_still_denied_registry_entry_to_dict(item: ActivationStillDeniedRegistryEntry) -> dict:
    return {
        "registry_entry_id": item.registry_entry_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "queue_item_id": item.queue_item_id,
        "bundle_id": item.bundle_id,
        "source_checkpoint_id": item.source_checkpoint_id,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "denial_reason": item.denial_reason,
        "required_followups": item.required_followups,
        "safety_flags": [f.value for f in item.safety_flags],
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def readiness_confirmation_audit_entry_to_dict(item: ReadinessConfirmationAuditEntry) -> dict:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "action": item.action,
        "decision": item.decision,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def readiness_confirmation_review_to_dict(item: ReadinessConfirmationReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "queue_items": [readiness_confirmation_queue_item_to_dict(q) for q in item.queue_items],
        "bundles": [human_review_bundle_to_dict(b) for b in item.bundles],
        "checklist_items": [human_review_checklist_item_to_dict(c) for c in item.checklist_items],
        "reviewer_notes": [reviewer_note_to_dict(n) for n in item.reviewer_notes],
        "registry_entries": [activation_still_denied_registry_entry_to_dict(e) for e in item.registry_entries],
        "audit_entries": [readiness_confirmation_audit_entry_to_dict(a) for a in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_readiness_confirmation_queue_item(item: ReadinessConfirmationQueueItem) -> None:
    if not item.activation_denied_required:
        raise ValueError("activation_denied_required must be True for queue item.")
    if not item.manual_review_required:
        raise ValueError("manual_review_required must be True for queue item.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Queue item must not allow active execution.")

def validate_human_review_bundle(item: HumanReviewBundle) -> None:
    if not item.activation_denied:
        raise ValueError("activation_denied must be True for bundle.")
    if item.activation_allowed:
        raise ValueError("activation_allowed must be False for bundle.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Bundle must not allow active execution.")

def validate_human_review_checklist_item(item: HumanReviewChecklistItem) -> None:
    pass

def validate_reviewer_note(item: ReviewerNote) -> None:
    pass

def validate_activation_still_denied_registry_entry(item: ActivationStillDeniedRegistryEntry) -> None:
    if not item.activation_denied:
        raise ValueError("activation_denied must be True for registry entry.")
    if item.activation_allowed:
        raise ValueError("activation_allowed must be False for registry entry.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Registry entry must not allow active execution.")

def validate_readiness_confirmation_review(item: ReadinessConfirmationReview) -> None:
    for q in item.queue_items:
        validate_readiness_confirmation_queue_item(q)
    for b in item.bundles:
        validate_human_review_bundle(b)
    for c in item.checklist_items:
        validate_human_review_checklist_item(c)
    for n in item.reviewer_notes:
        validate_reviewer_note(n)
    for e in item.registry_entries:
        validate_activation_still_denied_registry_entry(e)

def create_readiness_confirmation_queue_item_id(prefix: str = "readiness_confirmation_queue") -> str:
    return f"{prefix}_{uuid4()}"

def create_human_review_bundle_id(prefix: str = "human_review_bundle") -> str:
    return f"{prefix}_{uuid4()}"

def create_human_review_checklist_item_id(prefix: str = "human_review_checklist") -> str:
    return f"{prefix}_{uuid4()}"

def create_reviewer_note_id(prefix: str = "reviewer_note") -> str:
    return f"{prefix}_{uuid4()}"

def create_activation_still_denied_registry_entry_id(prefix: str = "activation_still_denied") -> str:
    return f"{prefix}_{uuid4()}"

def create_readiness_confirmation_audit_id(prefix: str = "readiness_confirmation_audit") -> str:
    return f"{prefix}_{uuid4()}"

def create_readiness_confirmation_review_id(prefix: str = "readiness_confirmation_review") -> str:
    return f"{prefix}_{uuid4()}"
