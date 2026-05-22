
from dataclasses import dataclass, field
from typing import Any, List, Optional
import datetime
import uuid

from usa_signal_bot.core.enums import (
    PaperReadinessBoardStatus, PaperReadinessBoardDecision, ReadinessBoardGateStatus,
    WriteBlockedAdapterStatus, RuntimeWriteAttemptType, WriteBlockAction,
    ActivationFirewallStatus, ActivationAttemptType, ActivationFirewallDecision,
    PaperReadinessBoardRiskFlag, PaperReadinessBoardReportType
)

@dataclass
class PaperReadinessBoardGate:
    gate_id: str
    created_at_utc: str
    gate_name: str
    status: ReadinessBoardGateStatus
    observed_value: Any
    expected_value: Any
    description: str
    required: bool
    risk_flags: List[PaperReadinessBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class WriteBlockedRuntimeAdapterProof:
    proof_id: str
    created_at_utc: str
    status: WriteBlockedAdapterStatus
    candidate_id: Optional[str]
    read_only_snapshot_hash: Optional[str]
    write_attempt_types_tested: List[str]
    blocked_write_attempt_count: int
    unblocked_write_attempt_count: int
    all_writes_blocked: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    risk_flags: List[PaperReadinessBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class RuntimeWriteBlockEvent:
    event_id: str
    created_at_utc: str
    attempt_type: RuntimeWriteAttemptType
    action: WriteBlockAction
    blocked: bool
    source_component: Optional[str]
    description: str
    payload_summary: dict
    risk_flags: List[PaperReadinessBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class ActivationFirewallRule:
    rule_id: str
    created_at_utc: str
    attempt_type: ActivationAttemptType
    enabled: bool
    blocking: bool
    decision: ActivationFirewallDecision
    description: str
    risk_flags: List[PaperReadinessBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class ActivationFirewallEvent:
    event_id: str
    created_at_utc: str
    attempt_type: ActivationAttemptType
    status: ActivationFirewallStatus
    decision: ActivationFirewallDecision
    blocked: bool
    activation_allowed: bool
    source_component: Optional[str]
    description: str
    payload_summary: dict
    risk_flags: List[PaperReadinessBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class PaperReadinessBoardReview:
    board_review_id: str
    created_at_utc: str
    status: PaperReadinessBoardStatus
    decision: PaperReadinessBoardDecision
    candidate_id: Optional[str]
    source_confirmation_review_id: Optional[str]
    source_human_review_bundle_id: Optional[str]
    source_activation_denied_registry_id: Optional[str]
    gates: List[PaperReadinessBoardGate]
    write_block_proofs: List[WriteBlockedRuntimeAdapterProof]
    activation_firewall_events: List[ActivationFirewallEvent]
    readiness_confidence: Optional[str]
    evidence_refs: List[str]
    required_followups: List[str]
    safety_flags: List[PaperReadinessBoardRiskFlag]
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class PaperReadinessBoardAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[PaperReadinessBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict = field(default_factory=dict)

@dataclass
class PaperReadinessBoardFullReview:
    review_id: str
    created_at_utc: str
    report_type: PaperReadinessBoardReportType
    board_reviews: List[PaperReadinessBoardReview]
    gates: List[PaperReadinessBoardGate]
    write_block_events: List[RuntimeWriteBlockEvent]
    write_block_proofs: List[WriteBlockedRuntimeAdapterProof]
    activation_firewall_rules: List[ActivationFirewallRule]
    activation_firewall_events: List[ActivationFirewallEvent]
    audit_entries: List[PaperReadinessBoardAuditEntry]
    output_paths: dict
    warnings: List[str]
    errors: List[str]

# Functions
def paper_readiness_board_gate_to_dict(item: PaperReadinessBoardGate) -> dict: return item.__dict__
def write_blocked_runtime_adapter_proof_to_dict(item: WriteBlockedRuntimeAdapterProof) -> dict: return item.__dict__
def runtime_write_block_event_to_dict(item: RuntimeWriteBlockEvent) -> dict: return item.__dict__
def activation_firewall_rule_to_dict(item: ActivationFirewallRule) -> dict: return item.__dict__
def activation_firewall_event_to_dict(item: ActivationFirewallEvent) -> dict: return item.__dict__
def paper_readiness_board_review_to_dict(item: PaperReadinessBoardReview) -> dict: return item.__dict__
def paper_readiness_board_audit_entry_to_dict(item: PaperReadinessBoardAuditEntry) -> dict: return item.__dict__
def paper_readiness_board_full_review_to_dict(item: PaperReadinessBoardFullReview) -> dict: return item.__dict__

def validate_paper_readiness_board_gate(item: PaperReadinessBoardGate) -> None: pass
def validate_write_blocked_runtime_adapter_proof(item: WriteBlockedRuntimeAdapterProof) -> None:
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Adapter proof must strictly disallow any execution or state mutation.")
    if not item.all_writes_blocked or item.unblocked_write_attempt_count > 0:
        raise ValueError("All write attempts must be blocked.")

def validate_runtime_write_block_event(item: RuntimeWriteBlockEvent) -> None: pass
def validate_activation_firewall_rule(item: ActivationFirewallRule) -> None:
    if not item.enabled or not item.blocking:
        raise ValueError("Firewall rule must be enabled and blocking.")

def validate_activation_firewall_event(item: ActivationFirewallEvent) -> None:
    if not item.blocked or item.activation_allowed:
        raise ValueError("Firewall event must be blocked and activation_allowed must be false.")

def validate_paper_readiness_board_review(item: PaperReadinessBoardReview) -> None:
    if not item.activation_denied: raise ValueError("activation_denied must be True")
    if item.activation_allowed: raise ValueError("activation_allowed must be False")
    if not item.manual_review_required: raise ValueError("manual_review_required must be True")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("All execution capabilities must be false.")

def validate_paper_readiness_board_full_review(item: PaperReadinessBoardFullReview) -> None: pass

def create_board_gate_id(prefix: str = "paper_readiness_board_gate") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_write_block_proof_id(prefix: str = "write_block_proof") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_runtime_write_block_event_id(prefix: str = "runtime_write_block_event") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_activation_firewall_rule_id(prefix: str = "activation_firewall_rule") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_activation_firewall_event_id(prefix: str = "activation_firewall_event") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_board_review_id(prefix: str = "paper_readiness_board_review") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_board_audit_id(prefix: str = "paper_readiness_board_audit") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_board_full_review_id(prefix: str = "paper_readiness_board_full_review") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
