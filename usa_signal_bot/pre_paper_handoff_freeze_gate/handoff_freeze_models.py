from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from usa_signal_bot.core.enums import (
    SandboxRuntimeAdmissionReplayDecision,
    SandboxRuntimeAdmissionReplayStatus,
    SandboxRuntimeAdmissionReplayOutcome,
    PrePaperHandoffFreezeRiskFlag,
    SimulatorEvidenceFreezeStatus,
    SimulatorEvidenceFreezeDecision,
    HandoffFreezeRuleStatus,
    HandoffFreezeAssertionStatus,
    PrePaperHandoffFreezeGateStatus,
    PrePaperHandoffFreezeGateDecision,
    PrePaperHandoffFreezeReportType
)

@dataclass
class SandboxRuntimeAdmissionReplayItem:
    replay_item_id: str
    created_at_utc: str
    attempt_type: str
    source_event_id: Optional[str]
    decision: SandboxRuntimeAdmissionReplayDecision
    blocked: bool
    sandbox_runtime_admission_allowed: bool
    paper_sandbox_runtime_allowed: bool
    simulator_admission_allowed: bool
    local_paper_simulator_allowed: bool
    admission_allowed: bool
    active_paper_enabled: bool
    order_created: bool
    paper_state_mutated: bool
    broker_order_sent: bool
    telegram_real_sent: bool
    config_patched: bool
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxRuntimeAdmissionReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    source_simulator_dossier_id: Optional[str]
    source_acceptance_seal_id: Optional[str]
    required_attempt_types: List[str]
    require_all_attempts_blocked: bool
    execution_enabled: bool
    sandbox_runtime_admission_enabled: bool
    paper_sandbox_runtime_enabled: bool
    simulator_admission_enabled: bool
    local_paper_simulator_enabled: bool
    active_paper_enabled: bool
    paper_admission_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    telegram_real_send_enabled: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxRuntimeAdmissionReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: Optional[str]
    status: SandboxRuntimeAdmissionReplayStatus
    outcome: SandboxRuntimeAdmissionReplayOutcome
    replayed_attempt_count: int
    blocked_attempt_count: int
    allowed_attempt_count: int
    missing_event_count: int
    passed: bool
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorEvidenceFreezeItem:
    freeze_item_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: Optional[str]
    source_path: Optional[str]
    frozen: bool
    immutable: bool
    available: bool
    fresh: bool
    stale: bool
    item_hash: Optional[str]
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorEvidenceFreezeBundle:
    freeze_id: str
    created_at_utc: str
    status: SimulatorEvidenceFreezeStatus
    decision: SimulatorEvidenceFreezeDecision
    candidate_id: Optional[str]
    source_simulator_dossier_id: Optional[str]
    items: List[SimulatorEvidenceFreezeItem]
    evidence_refs: List[str]
    freeze_hash: Optional[str]
    frozen: bool
    immutable: bool
    freeze_is_metadata_only: bool
    missing_evidence_count: int
    stale_evidence_count: int
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HandoffFreezeRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: HandoffFreezeRuleStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    required: bool
    description: str
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HandoffFreezeAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: HandoffFreezeAssertionStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    description: str
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalPrePaperHandoffFreezeGate:
    gate_id: str
    created_at_utc: str
    status: PrePaperHandoffFreezeGateStatus
    decision: PrePaperHandoffFreezeGateDecision
    candidate_id: Optional[str]
    source_simulator_dossier_review_id: Optional[str]
    source_simulator_dossier_id: Optional[str]
    source_simulator_acceptance_seal_id: Optional[str]
    source_sandbox_replay_result_id: Optional[str]
    source_simulator_evidence_freeze_id: Optional[str]
    sandbox_replay_result: Optional[SandboxRuntimeAdmissionReplayResult]
    evidence_freeze: Optional[SimulatorEvidenceFreezeBundle]
    rules: List[HandoffFreezeRule]
    assertions: List[HandoffFreezeAssertion]
    gate_hash: Optional[str]
    sealed: bool
    immutable: bool
    frozen: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    sandbox_runtime_admission_allowed: bool
    paper_sandbox_runtime_allowed: bool
    simulator_admission_allowed: bool
    local_paper_simulator_allowed: bool
    active_paper_enabled: bool
    pre_paper_handoff_complete: bool
    handoff_is_metadata_only: bool
    simulator_dossier_valid: bool
    simulator_acceptance_seal_valid: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: List[PrePaperHandoffFreezeRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperHandoffFreezeAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[PrePaperHandoffFreezeRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperHandoffFreezeFullReview:
    review_id: str
    created_at_utc: str
    report_type: PrePaperHandoffFreezeReportType
    gates: List[FinalPrePaperHandoffFreezeGate]
    sandbox_replay_plans: List[SandboxRuntimeAdmissionReplayPlan]
    sandbox_replay_results: List[SandboxRuntimeAdmissionReplayResult]
    sandbox_replay_items: List[SandboxRuntimeAdmissionReplayItem]
    evidence_freezes: List[SimulatorEvidenceFreezeBundle]
    rules: List[HandoffFreezeRule]
    assertions: List[HandoffFreezeAssertion]
    audit_entries: List[PrePaperHandoffFreezeAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

from usa_signal_bot.core.serialization import dataclass_to_dict

def sandbox_runtime_admission_replay_item_to_dict(item: SandboxRuntimeAdmissionReplayItem) -> dict:
    return dataclass_to_dict(item)

def sandbox_runtime_admission_replay_plan_to_dict(item: SandboxRuntimeAdmissionReplayPlan) -> dict:
    return dataclass_to_dict(item)

def sandbox_runtime_admission_replay_result_to_dict(item: SandboxRuntimeAdmissionReplayResult) -> dict:
    return dataclass_to_dict(item)

def simulator_evidence_freeze_item_to_dict(item: SimulatorEvidenceFreezeItem) -> dict:
    return dataclass_to_dict(item)

def simulator_evidence_freeze_bundle_to_dict(item: SimulatorEvidenceFreezeBundle) -> dict:
    return dataclass_to_dict(item)

def handoff_freeze_rule_to_dict(item: HandoffFreezeRule) -> dict:
    return dataclass_to_dict(item)

def handoff_freeze_assertion_to_dict(item: HandoffFreezeAssertion) -> dict:
    return dataclass_to_dict(item)

def final_pre_paper_handoff_freeze_gate_to_dict(item: FinalPrePaperHandoffFreezeGate) -> dict:
    return dataclass_to_dict(item)

def pre_paper_handoff_freeze_audit_entry_to_dict(item: PrePaperHandoffFreezeAuditEntry) -> dict:
    return dataclass_to_dict(item)

def pre_paper_handoff_freeze_full_review_to_dict(item: PrePaperHandoffFreezeFullReview) -> dict:
    return dataclass_to_dict(item)

import uuid

def create_sandbox_replay_item_id(prefix: str = "sandbox_runtime_replay_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_replay_plan_id(prefix: str = "sandbox_runtime_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_replay_result_id(prefix: str = "sandbox_runtime_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_evidence_freeze_item_id(prefix: str = "simulator_evidence_freeze_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_evidence_freeze_id(prefix: str = "simulator_evidence_freeze") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_handoff_freeze_rule_id(prefix: str = "handoff_freeze_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_handoff_freeze_assertion_id(prefix: str = "handoff_freeze_assertion") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_final_handoff_freeze_gate_id(prefix: str = "final_pre_paper_handoff_freeze_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_handoff_freeze_audit_id(prefix: str = "handoff_freeze_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_handoff_freeze_full_review_id(prefix: str = "handoff_freeze_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_sandbox_runtime_admission_replay_item(item: SandboxRuntimeAdmissionReplayItem) -> None:
    pass

def validate_sandbox_runtime_admission_replay_plan(item: SandboxRuntimeAdmissionReplayPlan) -> None:
    pass

def validate_sandbox_runtime_admission_replay_result(item: SandboxRuntimeAdmissionReplayResult) -> None:
    pass

def validate_simulator_evidence_freeze_bundle(item: SimulatorEvidenceFreezeBundle) -> None:
    pass

def validate_handoff_freeze_rule(item: HandoffFreezeRule) -> None:
    pass

def validate_handoff_freeze_assertion(item: HandoffFreezeAssertion) -> None:
    pass

def validate_final_pre_paper_handoff_freeze_gate(item: FinalPrePaperHandoffFreezeGate) -> None:
    pass

def validate_pre_paper_handoff_freeze_full_review(item: PrePaperHandoffFreezeFullReview) -> None:
    pass
