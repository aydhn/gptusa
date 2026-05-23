from dataclasses import dataclass, field
from typing import Any, Optional
import uuid

from usa_signal_bot.core.enums import (
    PaperSandboxBoundaryCertificateStatus,
    PaperSandboxBoundaryDecision,
    AdmissionBlockerReplayStatus,
    AdmissionBlockerReplayOutcome,
    NoOrderEvidenceFreezeStatus,
    NoOrderEvidenceFreezeDecision,
    BoundaryRuleStatus,
    BoundaryAssertionStatus,
    PaperSandboxBoundaryRiskFlag,
    PaperSandboxBoundaryReportType
)

@dataclass
class AdmissionBlockerReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    source_no_order_dossier_id: Optional[str]
    source_blocker_rule_refs: list[str]
    required_attempt_types: list[str]
    require_all_attempts_blocked: bool
    execution_enabled: bool
    active_paper_enabled: bool
    paper_admission_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    telegram_real_send_enabled: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AdmissionBlockerReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: Optional[str]
    status: AdmissionBlockerReplayStatus
    outcome: AdmissionBlockerReplayOutcome
    replayed_attempt_count: int
    blocked_attempt_count: int
    allowed_attempt_count: int
    missing_rule_count: int
    passed: bool
    risk_flags: list[PaperSandboxBoundaryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoOrderEvidenceFreezeItem:
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
    risk_flags: list[PaperSandboxBoundaryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoOrderEvidenceFreezeBundle:
    freeze_id: str
    created_at_utc: str
    status: NoOrderEvidenceFreezeStatus
    decision: NoOrderEvidenceFreezeDecision
    candidate_id: Optional[str]
    source_no_order_dossier_id: Optional[str]
    items: list[NoOrderEvidenceFreezeItem]
    evidence_refs: list[str]
    freeze_hash: Optional[str]
    frozen: bool
    immutable: bool
    freeze_is_metadata_only: bool
    missing_evidence_count: int
    stale_evidence_count: int
    risk_flags: list[PaperSandboxBoundaryRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: BoundaryRuleStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    required: bool
    description: str
    risk_flags: list[PaperSandboxBoundaryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoundaryAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: BoundaryAssertionStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    description: str
    risk_flags: list[PaperSandboxBoundaryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSandboxBoundaryCertificate:
    certificate_id: str
    created_at_utc: str
    status: PaperSandboxBoundaryCertificateStatus
    decision: PaperSandboxBoundaryDecision
    candidate_id: Optional[str]
    source_no_order_review_id: Optional[str]
    source_no_order_dossier_id: Optional[str]
    source_replay_seal_id: Optional[str]
    source_freeze_id: Optional[str]
    blocker_replay_result: Optional[AdmissionBlockerReplayResult]
    evidence_freeze: Optional[NoOrderEvidenceFreezeBundle]
    boundary_rules: list[BoundaryRule]
    boundary_assertions: list[BoundaryAssertion]
    certificate_hash: Optional[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[PaperSandboxBoundaryRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoundaryAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[PaperSandboxBoundaryRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoundaryCertificateFullReview:
    review_id: str
    created_at_utc: str
    report_type: PaperSandboxBoundaryReportType
    certificates: list[PaperSandboxBoundaryCertificate]
    replay_plans: list[AdmissionBlockerReplayPlan]
    replay_results: list[AdmissionBlockerReplayResult]
    evidence_freezes: list[NoOrderEvidenceFreezeBundle]
    boundary_rules: list[BoundaryRule]
    boundary_assertions: list[BoundaryAssertion]
    audit_entries: list[BoundaryAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

# Conversion functions
from usa_signal_bot.core.serialization import dataclass_to_dict as to_dict_clean

def admission_blocker_replay_plan_to_dict(item: AdmissionBlockerReplayPlan) -> dict:
    return to_dict_clean(item)

def admission_blocker_replay_result_to_dict(item: AdmissionBlockerReplayResult) -> dict:
    return to_dict_clean(item)

def no_order_evidence_freeze_item_to_dict(item: NoOrderEvidenceFreezeItem) -> dict:
    return to_dict_clean(item)

def no_order_evidence_freeze_bundle_to_dict(item: NoOrderEvidenceFreezeBundle) -> dict:
    return to_dict_clean(item)

def boundary_rule_to_dict(item: BoundaryRule) -> dict:
    return to_dict_clean(item)

def boundary_assertion_to_dict(item: BoundaryAssertion) -> dict:
    return to_dict_clean(item)

def paper_sandbox_boundary_certificate_to_dict(item: PaperSandboxBoundaryCertificate) -> dict:
    return to_dict_clean(item)

def boundary_audit_entry_to_dict(item: BoundaryAuditEntry) -> dict:
    return to_dict_clean(item)

def boundary_certificate_full_review_to_dict(item: BoundaryCertificateFullReview) -> dict:
    return to_dict_clean(item)

# ID Generators
def create_blocker_replay_plan_id(prefix: str = "blocker_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_blocker_replay_result_id(prefix: str = "blocker_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_evidence_freeze_item_id(prefix: str = "evidence_freeze_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_evidence_freeze_id(prefix: str = "no_order_evidence_freeze") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_boundary_rule_id(prefix: str = "boundary_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_boundary_assertion_id(prefix: str = "boundary_assertion") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_boundary_certificate_id(prefix: str = "paper_sandbox_boundary_certificate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_boundary_audit_id(prefix: str = "boundary_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_boundary_full_review_id(prefix: str = "boundary_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# Validation
from usa_signal_bot.core.exceptions import BoundaryCertificateValidationError

def validate_admission_blocker_replay_plan(item: AdmissionBlockerReplayPlan) -> None:
    if item.execution_enabled or item.active_paper_enabled or item.paper_admission_enabled or item.broker_execution_enabled or item.paper_state_mutation_enabled or item.config_patch_enabled or item.telegram_real_send_enabled:
        raise BoundaryCertificateValidationError("Replay plan execution flags must all be False.")

def validate_admission_blocker_replay_result(item: AdmissionBlockerReplayResult) -> None:
    if item.passed and item.allowed_attempt_count > 0:
        raise BoundaryCertificateValidationError("Replay result passed but allowed_attempt_count > 0.")

def validate_no_order_evidence_freeze_item(item: NoOrderEvidenceFreezeItem) -> None:
    pass

def validate_no_order_evidence_freeze_bundle(item: NoOrderEvidenceFreezeBundle) -> None:
    if not item.frozen or not item.immutable or not item.freeze_is_metadata_only:
        raise BoundaryCertificateValidationError("Evidence freeze must be frozen, immutable and metadata only.")

def validate_boundary_rule(item: BoundaryRule) -> None:
    pass

def validate_boundary_assertion(item: BoundaryAssertion) -> None:
    pass

def validate_paper_sandbox_boundary_certificate(item: PaperSandboxBoundaryCertificate) -> None:
    if item.sealed and not item.immutable:
        raise BoundaryCertificateValidationError("Sealed certificate must be immutable.")
    if not item.manual_review_required:
        raise BoundaryCertificateValidationError("Manual review required must be True.")
    if not item.activation_denied:
        raise BoundaryCertificateValidationError("Activation denied must be True.")
    if item.activation_allowed:
        raise BoundaryCertificateValidationError("Activation allowed must be False.")
    if item.admission_allowed:
        raise BoundaryCertificateValidationError("Admission allowed must be False.")
    if item.transition_allowed:
        raise BoundaryCertificateValidationError("Transition allowed must be False.")
    if not item.all_writes_blocked:
        raise BoundaryCertificateValidationError("All writes blocked must be True.")
    if item.order_created:
        raise BoundaryCertificateValidationError("Order created must be False.")
    if item.mutation_detected:
        raise BoundaryCertificateValidationError("Mutation detected must be False.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise BoundaryCertificateValidationError("Certificate allows dangerous operations.")

def validate_boundary_certificate_full_review(item: BoundaryCertificateFullReview) -> None:
    pass


# --- Phase 92 ---
# Phase 92