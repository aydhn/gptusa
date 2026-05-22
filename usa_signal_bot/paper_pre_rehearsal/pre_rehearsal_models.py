from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import datetime
import uuid

from usa_signal_bot.core.enums import (
    PrePaperDryRehearsalStatus,
    PrePaperDryRehearsalDecision,
    MutationAttemptType,
    FirewallAction,
    ActivationDeniedCheckpointStatus,
    ActivationDeniedDecision,
    PrePaperRiskFlag,
    PrePaperReportType
)

@dataclass
class PrePaperDryRehearsalPlan:
    plan_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    source_checkpoint_id: Optional[str]
    source_archive_id: Optional[str]
    status: PrePaperDryRehearsalStatus
    decision: PrePaperDryRehearsalDecision
    required_inputs: List[str]
    expected_outputs: List[str]
    firewall_required: bool
    activation_denied_required: bool
    execution_enabled: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    telegram_real_send_enabled: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MutationFirewallRule:
    rule_id: str
    created_at_utc: str
    attempt_type: MutationAttemptType
    action: FirewallAction
    enabled: bool
    blocking: bool
    description: str
    risk_flags: List[PrePaperRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MutationFirewallEvent:
    event_id: str
    created_at_utc: str
    attempt_type: MutationAttemptType
    action: FirewallAction
    blocked: bool
    session_id: Optional[str]
    source_component: Optional[str]
    description: str
    risk_flags: List[PrePaperRiskFlag]
    payload_summary: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperDryRehearsalRun:
    run_id: str
    created_at_utc: str
    status: PrePaperDryRehearsalStatus
    candidate_id: Optional[str]
    plan: Optional[PrePaperDryRehearsalPlan]
    firewall_rules: List[MutationFirewallRule]
    firewall_events: List[MutationFirewallEvent]
    read_only_paper_baseline: Dict[str, Any]
    output_summary: Dict[str, Any]
    decision: PrePaperDryRehearsalDecision
    safety_flags: List[PrePaperRiskFlag]
    started_at_utc: Optional[str]
    completed_at_utc: Optional[str]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ActivationDeniedCheckpoint:
    checkpoint_id: str
    created_at_utc: str
    status: ActivationDeniedCheckpointStatus
    decision: ActivationDeniedDecision
    candidate_id: Optional[str]
    source_run_id: Optional[str]
    source_plan_id: Optional[str]
    activation_denied: bool
    denial_reason: str
    required_followups: List[str]
    safety_flags: List[PrePaperRiskFlag]
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[PrePaperRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperDryRehearsalReview:
    review_id: str
    created_at_utc: str
    report_type: PrePaperReportType
    plans: List[PrePaperDryRehearsalPlan]
    runs: List[PrePaperDryRehearsalRun]
    firewall_events: List[MutationFirewallEvent]
    activation_checkpoints: List[ActivationDeniedCheckpoint]
    audit_entries: List[PrePaperAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

import json
import dataclasses

def to_dict(obj: Any) -> Dict[str, Any]:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    return obj

def pre_paper_dry_rehearsal_plan_to_dict(item: PrePaperDryRehearsalPlan) -> dict:
    return to_dict(item)

def mutation_firewall_rule_to_dict(item: MutationFirewallRule) -> dict:
    return to_dict(item)

def mutation_firewall_event_to_dict(item: MutationFirewallEvent) -> dict:
    return to_dict(item)

def pre_paper_dry_rehearsal_run_to_dict(item: PrePaperDryRehearsalRun) -> dict:
    return to_dict(item)

def activation_denied_checkpoint_to_dict(item: ActivationDeniedCheckpoint) -> dict:
    return to_dict(item)

def pre_paper_audit_entry_to_dict(item: PrePaperAuditEntry) -> dict:
    return to_dict(item)

def pre_paper_dry_rehearsal_review_to_dict(item: PrePaperDryRehearsalReview) -> dict:
    return to_dict(item)

def validate_pre_paper_dry_rehearsal_plan(item: PrePaperDryRehearsalPlan) -> None:
    if item.execution_enabled:
        raise ValueError("execution_enabled must be false")
    if item.active_paper_enabled:
        raise ValueError("active_paper_enabled must be false")
    if item.broker_execution_enabled:
        raise ValueError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled:
        raise ValueError("paper_state_mutation_enabled must be false")
    if item.config_patch_enabled:
        raise ValueError("config_patch_enabled must be false")
    if item.telegram_real_send_enabled:
        raise ValueError("telegram_real_send_enabled must be false")
    if not item.firewall_required:
        raise ValueError("firewall_required must be true")
    if not item.activation_denied_required:
        raise ValueError("activation_denied_required must be true")

def validate_mutation_firewall_rule(item: MutationFirewallRule) -> None:
    if item.attempt_type in [
        MutationAttemptType.PAPER_STATE_WRITE,
        MutationAttemptType.PAPER_ORDER_CREATE,
        MutationAttemptType.PAPER_POSITION_MUTATION,
        MutationAttemptType.PAPER_PORTFOLIO_MUTATION,
        MutationAttemptType.PAPER_CASH_MUTATION,
        MutationAttemptType.PAPER_EQUITY_MUTATION,
        MutationAttemptType.PAPER_FILL_CREATE,
        MutationAttemptType.BROKER_ORDER_SEND,
        MutationAttemptType.TELEGRAM_REAL_SEND,
        MutationAttemptType.PRODUCTION_CONFIG_PATCH,
        MutationAttemptType.ACTIVE_PAPER_ENABLE,
        MutationAttemptType.OBSERVER_UNLOCK,
        MutationAttemptType.ARCHIVE_UNLOCK,
        MutationAttemptType.FINAL_LOCK_UNLOCK
    ]:
        if item.action not in [FirewallAction.DENY_AND_RECORD, FirewallAction.BLOCK_SESSION]:
            raise ValueError(f"Dangerous MutationAttemptType {item.attempt_type} must have DENY_AND_RECORD or BLOCK_SESSION action")

def validate_mutation_firewall_event(item: MutationFirewallEvent) -> None:
    pass

def validate_pre_paper_dry_rehearsal_run(item: PrePaperDryRehearsalRun) -> None:
    if item.plan:
        validate_pre_paper_dry_rehearsal_plan(item.plan)

def validate_activation_denied_checkpoint(item: ActivationDeniedCheckpoint) -> None:
    if not item.activation_denied:
        raise ValueError("activation_denied must be true")
    if item.allows_active_paper:
        raise ValueError("allows_active_paper must be false")
    if item.allows_broker_execution:
        raise ValueError("allows_broker_execution must be false")
    if item.allows_paper_state_mutation:
        raise ValueError("allows_paper_state_mutation must be false")
    if item.allows_config_patch:
        raise ValueError("allows_config_patch must be false")
    if item.allows_telegram_real_send:
        raise ValueError("allows_telegram_real_send must be false")

def validate_pre_paper_dry_rehearsal_review(item: PrePaperDryRehearsalReview) -> None:
    for plan in item.plans:
        validate_pre_paper_dry_rehearsal_plan(plan)
    for run in item.runs:
        validate_pre_paper_dry_rehearsal_run(run)
    for cp in item.activation_checkpoints:
        validate_activation_denied_checkpoint(cp)

def create_pre_paper_plan_id(prefix: str = "pre_paper_plan") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_mutation_firewall_rule_id(prefix: str = "mutation_firewall_rule") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_mutation_firewall_event_id(prefix: str = "mutation_firewall_event") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_pre_paper_run_id(prefix: str = "pre_paper_run") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_activation_denied_checkpoint_id(prefix: str = "activation_denied_checkpoint") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_pre_paper_audit_id(prefix: str = "pre_paper_audit") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_pre_paper_review_id(prefix: str = "pre_paper_review") -> str:
    return f"{prefix}_{uuid.uuid4()}"
