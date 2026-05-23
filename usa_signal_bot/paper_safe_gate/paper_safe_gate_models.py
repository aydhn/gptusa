
import uuid
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    BoundaryCertificateReplayStatus, BoundaryCertificateReplayOutcome,
    FrozenEvidenceIntegrityStatus, FrozenEvidenceIntegrityDecision,
    FinalPaperSafeGateStatus, FinalPaperSafeGateDecision,
    PaperSafeGateRuleStatus, PaperSafeGateAssertionStatus,
    PaperSafeGateRiskFlag, PaperSafeGateReportType
)
from usa_signal_bot.core.exceptions import (
    PaperSafeGateValidationError, BoundaryReplayPlanError
)

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class BoundaryCertificateReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    source_boundary_certificate_id: Optional[str]
    source_boundary_review_id: Optional[str]
    required_rule_names: List[str]
    required_assertion_names: List[str]
    require_all_rules_pass: bool
    require_all_assertions_pass: bool
    execution_enabled: bool
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
class BoundaryCertificateReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: Optional[str]
    status: BoundaryCertificateReplayStatus
    outcome: BoundaryCertificateReplayOutcome
    replayed_rule_count: int
    passed_rule_count: int
    failed_rule_count: int
    replayed_assertion_count: int
    passed_assertion_count: int
    failed_assertion_count: int
    missing_rule_count: int
    missing_assertion_count: int
    passed: bool
    risk_flags: List[PaperSafeGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FrozenEvidenceIntegrityItem:
    integrity_item_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: Optional[str]
    expected_hash: Optional[str]
    observed_hash: Optional[str]
    hash_matches: bool
    frozen: bool
    immutable: bool
    available: bool
    fresh: bool
    stale: bool
    tamper_detected: bool
    risk_flags: List[PaperSafeGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FrozenEvidenceIntegrityAudit:
    audit_id: str
    created_at_utc: str
    status: FrozenEvidenceIntegrityStatus
    decision: FrozenEvidenceIntegrityDecision
    candidate_id: Optional[str]
    source_freeze_id: Optional[str]
    source_boundary_certificate_id: Optional[str]
    items: List[FrozenEvidenceIntegrityItem]
    expected_freeze_hash: Optional[str]
    observed_freeze_hash: Optional[str]
    freeze_hash_matches: bool
    checked_item_count: int
    tamper_count: int
    missing_count: int
    stale_count: int
    frozen: bool
    immutable: bool
    integrity_valid: bool
    audit_is_metadata_only: bool
    risk_flags: List[PaperSafeGateRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeGateRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: PaperSafeGateRuleStatus
    expected_value: Any
    observed_value: Any
    required: bool
    description: str
    risk_flags: List[PaperSafeGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeGateAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: PaperSafeGateAssertionStatus
    expected_value: Any
    observed_value: Any
    description: str
    risk_flags: List[PaperSafeGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalPaperSafeGate:
    gate_id: str
    created_at_utc: str
    status: FinalPaperSafeGateStatus
    decision: FinalPaperSafeGateDecision
    candidate_id: Optional[str]
    source_boundary_review_id: Optional[str]
    source_boundary_certificate_id: Optional[str]
    source_replay_result_id: Optional[str]
    source_integrity_audit_id: Optional[str]
    replay_result: Optional[BoundaryCertificateReplayResult]
    integrity_audit: Optional[FrozenEvidenceIntegrityAudit]
    rules: List[PaperSafeGateRule]
    assertions: List[PaperSafeGateAssertion]
    gate_hash: Optional[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    paper_safe_gate_passed: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: List[PaperSafeGateRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeGateAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[PaperSafeGateRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeGateFullReview:
    review_id: str
    created_at_utc: str
    report_type: PaperSafeGateReportType
    gates: List[FinalPaperSafeGate]
    replay_plans: List[BoundaryCertificateReplayPlan]
    replay_results: List[BoundaryCertificateReplayResult]
    integrity_audits: List[FrozenEvidenceIntegrityAudit]
    rules: List[PaperSafeGateRule]
    assertions: List[PaperSafeGateAssertion]
    audit_entries: List[PaperSafeGateAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Conversion Functions
def boundary_certificate_replay_plan_to_dict(item: BoundaryCertificateReplayPlan) -> dict: return asdict(item)
def boundary_certificate_replay_result_to_dict(item: BoundaryCertificateReplayResult) -> dict: return asdict(item)
def frozen_evidence_integrity_item_to_dict(item: FrozenEvidenceIntegrityItem) -> dict: return asdict(item)
def frozen_evidence_integrity_audit_to_dict(item: FrozenEvidenceIntegrityAudit) -> dict: return asdict(item)
def paper_safe_gate_rule_to_dict(item: PaperSafeGateRule) -> dict: return asdict(item)
def paper_safe_gate_assertion_to_dict(item: PaperSafeGateAssertion) -> dict: return asdict(item)
def final_paper_safe_gate_to_dict(item: FinalPaperSafeGate) -> dict: return asdict(item)
def paper_safe_gate_audit_entry_to_dict(item: PaperSafeGateAuditEntry) -> dict: return asdict(item)
def paper_safe_gate_full_review_to_dict(item: PaperSafeGateFullReview) -> dict: return asdict(item)

# ID Creators
def create_boundary_replay_plan_id(prefix="boundary_replay_plan"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_boundary_replay_result_id(prefix="boundary_replay_result"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_integrity_item_id(prefix="frozen_integrity_item"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_integrity_audit_id(prefix="frozen_integrity_audit"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_paper_safe_rule_id(prefix="paper_safe_rule"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_paper_safe_assertion_id(prefix="paper_safe_assertion"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_final_paper_safe_gate_id(prefix="final_paper_safe_gate"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_paper_safe_audit_id(prefix="paper_safe_audit"): return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_paper_safe_full_review_id(prefix="paper_safe_full_review"): return f"{prefix}_{uuid.uuid4().hex[:8]}"

# Validators
def validate_boundary_certificate_replay_plan(item: BoundaryCertificateReplayPlan) -> None:
    if item.execution_enabled or item.active_paper_enabled or item.paper_admission_enabled or item.broker_execution_enabled or item.paper_state_mutation_enabled or item.config_patch_enabled or item.telegram_real_send_enabled:
        raise BoundaryReplayPlanError("All execution flags must be false")

def validate_boundary_certificate_replay_result(item: BoundaryCertificateReplayResult) -> None:
    if item.passed and (item.failed_rule_count > 0 or item.failed_assertion_count > 0):
        raise PaperSafeGateValidationError("Result passed but failed rules/assertions exist")

def validate_frozen_evidence_integrity_item(item: FrozenEvidenceIntegrityItem) -> None:
    pass

def validate_frozen_evidence_integrity_audit(item: FrozenEvidenceIntegrityAudit) -> None:
    if not item.audit_is_metadata_only:
        raise PaperSafeGateValidationError("Audit must be metadata-only")
    if item.integrity_valid and item.tamper_count > 0:
        raise PaperSafeGateValidationError("Audit valid but tamper detected")

def validate_paper_safe_gate_rule(item: PaperSafeGateRule) -> None:
    pass

def validate_paper_safe_gate_assertion(item: PaperSafeGateAssertion) -> None:
    pass

def validate_final_paper_safe_gate(item: FinalPaperSafeGate) -> None:
    if item.sealed and not item.immutable:
        raise PaperSafeGateValidationError("Sealed gate must be immutable")
    if not item.manual_review_required:
        raise PaperSafeGateValidationError("Manual review required must be true")
    if not item.activation_denied:
        raise PaperSafeGateValidationError("Activation denied must be true")
    if item.activation_allowed or item.admission_allowed or item.transition_allowed:
        raise PaperSafeGateValidationError("Activation/Admission/Transition allowed must be false")
    if not item.all_writes_blocked:
        raise PaperSafeGateValidationError("All writes blocked must be true")
    if item.order_created or item.mutation_detected:
        raise PaperSafeGateValidationError("Order created/Mutation detected must be false")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise PaperSafeGateValidationError("All allows_* must be false")

def validate_paper_safe_gate_full_review(item: PaperSafeGateFullReview) -> None:
    pass
