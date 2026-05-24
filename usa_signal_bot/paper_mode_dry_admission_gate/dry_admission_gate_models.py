import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, List, Dict

from usa_signal_bot.core.enums import (
    ShadowLaunchReplayStatus,
    ShadowLaunchReplayOutcome,
    ShadowLaunchReplayDecision,
    BoardEvidenceFreezeStatus,
    BoardEvidenceFreezeDecision,
    PaperModeDryAdmissionGateStatus,
    PaperModeDryAdmissionGateDecision,
    DryAdmissionGateRuleStatus,
    DryAdmissionGateAssertionStatus,
    DryAdmissionGateRiskFlag,
    DryAdmissionGateReportType
)


@dataclass
class ShadowLaunchReplayItem:
    replay_item_id: str
    created_at_utc: str
    attempt_type: str
    decision: ShadowLaunchReplayDecision
    blocked: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    admission_allowed: bool
    active_paper_enabled: bool
    order_created: bool
    paper_state_mutated: bool
    broker_order_sent: bool
    telegram_real_sent: bool
    config_patched: bool
    risk_flags: List[DryAdmissionGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    source_event_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShadowLaunchReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    required_attempt_types: List[str]
    require_all_attempts_blocked: bool
    execution_enabled: bool
    shadow_launch_enabled: bool
    paper_mode_launch_enabled: bool
    active_paper_enabled: bool
    paper_admission_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    telegram_real_send_enabled: bool
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_board_dossier_id: Optional[str] = None
    source_acceptance_seal_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShadowLaunchReplayResult:
    replay_result_id: str
    created_at_utc: str
    status: ShadowLaunchReplayStatus
    outcome: ShadowLaunchReplayOutcome
    replayed_attempt_count: int
    blocked_attempt_count: int
    allowed_attempt_count: int
    missing_event_count: int
    passed: bool
    risk_flags: List[DryAdmissionGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    replay_plan_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BoardEvidenceFreezeItem:
    freeze_item_id: str
    created_at_utc: str
    evidence_type: str
    frozen: bool
    immutable: bool
    available: bool
    fresh: bool
    stale: bool
    risk_flags: List[DryAdmissionGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    source_ref_id: Optional[str] = None
    source_path: Optional[str] = None
    item_hash: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BoardEvidenceFreezeBundle:
    freeze_id: str
    created_at_utc: str
    status: BoardEvidenceFreezeStatus
    decision: BoardEvidenceFreezeDecision
    items: List[BoardEvidenceFreezeItem]
    evidence_refs: List[str]
    frozen: bool
    immutable: bool
    freeze_is_metadata_only: bool
    missing_evidence_count: int
    stale_evidence_count: int
    risk_flags: List[DryAdmissionGateRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_board_dossier_id: Optional[str] = None
    freeze_hash: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DryAdmissionGateRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: DryAdmissionGateRuleStatus
    required: bool
    description: str
    risk_flags: List[DryAdmissionGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    expected_value: Optional[Any] = None
    observed_value: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DryAdmissionGateAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: DryAdmissionGateAssertionStatus
    description: str
    risk_flags: List[DryAdmissionGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    expected_value: Optional[Any] = None
    observed_value: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FinalPaperModeDryAdmissionGate:
    gate_id: str
    created_at_utc: str
    status: PaperModeDryAdmissionGateStatus
    decision: PaperModeDryAdmissionGateDecision
    rules: List[DryAdmissionGateRule]
    assertions: List[DryAdmissionGateAssertion]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    dry_admission_gate_passed: bool
    board_dossier_valid: bool
    acceptance_seal_valid: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: List[DryAdmissionGateRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_board_dossier_review_id: Optional[str] = None
    source_board_dossier_id: Optional[str] = None
    source_acceptance_seal_id: Optional[str] = None
    source_shadow_replay_result_id: Optional[str] = None
    source_evidence_freeze_id: Optional[str] = None
    shadow_replay_result: Optional[ShadowLaunchReplayResult] = None
    evidence_freeze: Optional[BoardEvidenceFreezeBundle] = None
    gate_hash: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DryAdmissionGateAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[DryAdmissionGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    decision: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DryAdmissionGateFullReview:
    review_id: str
    created_at_utc: str
    report_type: DryAdmissionGateReportType
    gates: List[FinalPaperModeDryAdmissionGate]
    shadow_replay_plans: List[ShadowLaunchReplayPlan]
    shadow_replay_results: List[ShadowLaunchReplayResult]
    shadow_replay_items: List[ShadowLaunchReplayItem]
    evidence_freezes: List[BoardEvidenceFreezeBundle]
    rules: List[DryAdmissionGateRule]
    assertions: List[DryAdmissionGateAssertion]
    audit_entries: List[DryAdmissionGateAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


def shadow_launch_replay_item_to_dict(item: ShadowLaunchReplayItem) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def shadow_launch_replay_plan_to_dict(item: ShadowLaunchReplayPlan) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def shadow_launch_replay_result_to_dict(item: ShadowLaunchReplayResult) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def board_evidence_freeze_item_to_dict(item: BoardEvidenceFreezeItem) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def board_evidence_freeze_bundle_to_dict(item: BoardEvidenceFreezeBundle) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def dry_admission_gate_rule_to_dict(item: DryAdmissionGateRule) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def dry_admission_gate_assertion_to_dict(item: DryAdmissionGateAssertion) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def final_paper_mode_dry_admission_gate_to_dict(item: FinalPaperModeDryAdmissionGate) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def dry_admission_gate_audit_entry_to_dict(item: DryAdmissionGateAuditEntry) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def dry_admission_gate_full_review_to_dict(item: DryAdmissionGateFullReview) -> dict:
    from usa_signal_bot.core.serialization import to_dict
    return to_dict(item)

def validate_shadow_launch_replay_item(item: ShadowLaunchReplayItem) -> None:
    if not item.blocked and item.decision != ShadowLaunchReplayDecision.BLOCK:
        if item.shadow_launch_allowed or item.paper_mode_launch_allowed:
            pass
        else:
            raise ValueError("Item blocked is False but it does not allow launch")
    if item.active_paper_enabled: raise ValueError("active_paper_enabled must be False")
    if item.order_created: raise ValueError("order_created must be False")
    if item.paper_state_mutated: raise ValueError("paper_state_mutated must be False")
    if item.broker_order_sent: raise ValueError("broker_order_sent must be False")
    if item.telegram_real_sent: raise ValueError("telegram_real_sent must be False")
    if item.config_patched: raise ValueError("config_patched must be False")

def validate_shadow_launch_replay_plan(item: ShadowLaunchReplayPlan) -> None:
    if item.execution_enabled: raise ValueError("execution_enabled must be False")
    if item.shadow_launch_enabled: raise ValueError("shadow_launch_enabled must be False")
    if item.paper_mode_launch_enabled: raise ValueError("paper_mode_launch_enabled must be False")
    if item.active_paper_enabled: raise ValueError("active_paper_enabled must be False")
    if item.paper_admission_enabled: raise ValueError("paper_admission_enabled must be False")
    if item.broker_execution_enabled: raise ValueError("broker_execution_enabled must be False")
    if item.paper_state_mutation_enabled: raise ValueError("paper_state_mutation_enabled must be False")
    if item.config_patch_enabled: raise ValueError("config_patch_enabled must be False")
    if item.telegram_real_send_enabled: raise ValueError("telegram_real_send_enabled must be False")

def validate_shadow_launch_replay_result(item: ShadowLaunchReplayResult) -> None:
    if item.passed and item.allowed_attempt_count > 0:
        raise ValueError("If passed, allowed_attempt_count must be 0")

def validate_board_evidence_freeze_bundle(item: BoardEvidenceFreezeBundle) -> None:
    if not item.frozen: raise ValueError("frozen must be True")
    if not item.immutable: raise ValueError("immutable must be True")
    if not item.freeze_is_metadata_only: raise ValueError("freeze_is_metadata_only must be True")

def validate_dry_admission_gate_rule(item: DryAdmissionGateRule) -> None:
    pass

def validate_dry_admission_gate_assertion(item: DryAdmissionGateAssertion) -> None:
    pass

def validate_final_paper_mode_dry_admission_gate(item: FinalPaperModeDryAdmissionGate) -> None:
    if item.sealed and not item.immutable: raise ValueError("If sealed, must be immutable")
    if not item.manual_review_required: raise ValueError("manual_review_required must be True")
    if not item.activation_denied: raise ValueError("activation_denied must be True")
    if item.activation_allowed: raise ValueError("activation_allowed must be False")
    if item.admission_allowed: raise ValueError("admission_allowed must be False")
    if item.transition_allowed: raise ValueError("transition_allowed must be False")
    if item.shadow_launch_allowed: raise ValueError("shadow_launch_allowed must be False")
    if item.paper_mode_launch_allowed: raise ValueError("paper_mode_launch_allowed must be False")
    if not item.dry_admission_gate_passed: raise ValueError("dry_admission_gate_passed must be True")
    if not item.board_dossier_valid: raise ValueError("board_dossier_valid must be True")
    if not item.acceptance_seal_valid: raise ValueError("acceptance_seal_valid must be True")
    if not item.all_writes_blocked: raise ValueError("all_writes_blocked must be True")
    if item.order_created: raise ValueError("order_created must be False")
    if item.mutation_detected: raise ValueError("mutation_detected must be False")
    if item.allows_active_paper: raise ValueError("allows_active_paper must be False")
    if item.allows_broker_execution: raise ValueError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation: raise ValueError("allows_paper_state_mutation must be False")
    if item.allows_config_patch: raise ValueError("allows_config_patch must be False")
    if item.allows_telegram_real_send: raise ValueError("allows_telegram_real_send must be False")

def validate_dry_admission_gate_full_review(item: DryAdmissionGateFullReview) -> None:
    for gate in item.gates:
        validate_final_paper_mode_dry_admission_gate(gate)

def create_shadow_replay_item_id(prefix: str = "shadow_replay_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_shadow_replay_plan_id(prefix: str = "shadow_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_shadow_replay_result_id(prefix: str = "shadow_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_board_evidence_freeze_item_id(prefix: str = "board_evidence_freeze_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_board_evidence_freeze_id(prefix: str = "board_evidence_freeze") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_dry_admission_rule_id(prefix: str = "dry_admission_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_dry_admission_assertion_id(prefix: str = "dry_admission_assertion") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_final_dry_admission_gate_id(prefix: str = "final_dry_admission_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_dry_admission_audit_id(prefix: str = "dry_admission_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

def create_dry_admission_full_review_id(prefix: str = "dry_admission_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"
