from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RehearsalReplayStatus,
    RehearsalReplayOutcome,
    RehearsalReplayDecision,
    DryAdmissionEvidenceFreezeStatus,
    DryAdmissionEvidenceFreezeDecision,
    LocalPaperAdmissionSimulatorGateStatus,
    LocalPaperAdmissionSimulatorGateDecision,
    SimulatorGateRuleStatus,
    SimulatorGateAssertionStatus,
    SimulatorGateRiskFlag,
    SimulatorGateReportType
)
from usa_signal_bot.core.exceptions import (
    RehearsalReplayAnalyzerError,
    DryAdmissionEvidenceFreezeError,
    SimulatorGateRuleError,
    SimulatorGateAssertionError,
    FinalSimulatorGateError,
    SimulatorReportingError,
    RehearsalReplayEngineError
)

@dataclass
class RehearsalReplayItem:
    replay_item_id: str
    created_at_utc: str
    attempt_type: str
    source_event_id: str | None
    decision: RehearsalReplayDecision
    blocked: bool
    rehearsal_allowed: bool
    paper_mode_rehearsal_allowed: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    admission_allowed: bool
    active_paper_enabled: bool
    order_created: bool
    paper_state_mutated: bool
    broker_order_sent: bool
    telegram_real_sent: bool
    config_patched: bool
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RehearsalReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: str | None
    source_dry_admission_dossier_id: str | None
    source_acceptance_seal_id: str | None
    required_attempt_types: list[str] = field(default_factory=list)
    require_all_attempts_blocked: bool = True
    execution_enabled: bool = False
    rehearsal_enabled: bool = False
    paper_mode_rehearsal_enabled: bool = False
    shadow_launch_enabled: bool = False
    paper_mode_launch_enabled: bool = False
    active_paper_enabled: bool = False
    paper_admission_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RehearsalReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: str | None
    status: RehearsalReplayStatus
    outcome: RehearsalReplayOutcome
    replayed_attempt_count: int
    blocked_attempt_count: int
    allowed_attempt_count: int
    missing_event_count: int
    passed: bool
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionEvidenceFreezeItem:
    freeze_item_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: str | None
    source_path: str | None
    frozen: bool
    immutable: bool
    available: bool
    fresh: bool
    stale: bool
    item_hash: str | None
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionEvidenceFreezeBundle:
    freeze_id: str
    created_at_utc: str
    status: DryAdmissionEvidenceFreezeStatus
    decision: DryAdmissionEvidenceFreezeDecision
    candidate_id: str | None
    source_dry_admission_dossier_id: str | None
    items: list[DryAdmissionEvidenceFreezeItem] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    freeze_hash: str | None = None
    frozen: bool = False
    immutable: bool = False
    freeze_is_metadata_only: bool = False
    missing_evidence_count: int = 0
    stale_evidence_count: int = 0
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    required_followups: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorGateRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: SimulatorGateRuleStatus
    expected_value: Any | None
    observed_value: Any | None
    required: bool
    description: str
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorGateAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: SimulatorGateAssertionStatus
    expected_value: Any | None
    observed_value: Any | None
    description: str
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalLocalPaperAdmissionSimulatorGate:
    gate_id: str
    created_at_utc: str
    status: LocalPaperAdmissionSimulatorGateStatus
    decision: LocalPaperAdmissionSimulatorGateDecision
    candidate_id: str | None
    source_dry_admission_dossier_review_id: str | None
    source_dry_admission_dossier_id: str | None
    source_acceptance_seal_id: str | None
    source_rehearsal_replay_result_id: str | None
    source_evidence_freeze_id: str | None
    rehearsal_replay_result: RehearsalReplayResult | None = None
    evidence_freeze: DryAdmissionEvidenceFreezeBundle | None = None
    rules: list[SimulatorGateRule] = field(default_factory=list)
    assertions: list[SimulatorGateAssertion] = field(default_factory=list)
    gate_hash: str | None = None
    sealed: bool = False
    immutable: bool = False
    manual_review_required: bool = False
    activation_denied: bool = False
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    rehearsal_allowed: bool = False
    paper_mode_rehearsal_allowed: bool = False
    shadow_launch_allowed: bool = False
    paper_mode_launch_allowed: bool = False
    simulator_admission_allowed: bool = False
    local_paper_simulator_allowed: bool = False
    simulator_gate_passed: bool = False
    dry_admission_dossier_valid: bool = False
    dry_admission_acceptance_seal_valid: bool = False
    all_writes_blocked: bool = False
    order_created: bool = False
    mutation_detected: bool = False
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_paper_state_mutation: bool = False
    allows_config_patch: bool = False
    allows_telegram_real_send: bool = False
    safety_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    required_followups: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorGateAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: str | None
    rationale: str
    evidence_refs: list[str] = field(default_factory=list)
    risk_flags: list[SimulatorGateRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorGateFullReview:
    review_id: str
    created_at_utc: str
    report_type: SimulatorGateReportType
    gates: list[FinalLocalPaperAdmissionSimulatorGate] = field(default_factory=list)
    rehearsal_replay_plans: list[RehearsalReplayPlan] = field(default_factory=list)
    rehearsal_replay_results: list[RehearsalReplayResult] = field(default_factory=list)
    rehearsal_replay_items: list[RehearsalReplayItem] = field(default_factory=list)
    evidence_freezes: list[DryAdmissionEvidenceFreezeBundle] = field(default_factory=list)
    rules: list[SimulatorGateRule] = field(default_factory=list)
    assertions: list[SimulatorGateAssertion] = field(default_factory=list)
    audit_entries: list[SimulatorGateAuditEntry] = field(default_factory=list)
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_rehearsal_replay_item_id(prefix: str = "rehearsal_replay_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rehearsal_replay_plan_id(prefix: str = "rehearsal_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rehearsal_replay_result_id(prefix: str = "rehearsal_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_evidence_freeze_item_id(prefix: str = "dry_admission_evidence_freeze_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_evidence_freeze_id(prefix: str = "dry_admission_evidence_freeze") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_rule_id(prefix: str = "simulator_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_assertion_id(prefix: str = "simulator_assertion") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_final_simulator_gate_id(prefix: str = "final_simulator_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_audit_id(prefix: str = "simulator_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_full_review_id(prefix: str = "simulator_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def rehearsal_replay_item_to_dict(item: RehearsalReplayItem) -> dict:
    return {
        "replay_item_id": item.replay_item_id,
        "created_at_utc": item.created_at_utc,
        "attempt_type": item.attempt_type,
        "source_event_id": item.source_event_id,
        "decision": item.decision.value if isinstance(item.decision, RehearsalReplayDecision) else item.decision,
        "blocked": item.blocked,
        "rehearsal_allowed": item.rehearsal_allowed,
        "paper_mode_rehearsal_allowed": item.paper_mode_rehearsal_allowed,
        "shadow_launch_allowed": item.shadow_launch_allowed,
        "paper_mode_launch_allowed": item.paper_mode_launch_allowed,
        "admission_allowed": item.admission_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "broker_order_sent": item.broker_order_sent,
        "telegram_real_sent": item.telegram_real_sent,
        "config_patched": item.config_patched,
        "risk_flags": [f.value if isinstance(f, SimulatorGateRiskFlag) else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def rehearsal_replay_plan_to_dict(item: RehearsalReplayPlan) -> dict:
    return {
        "replay_plan_id": item.replay_plan_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "source_dry_admission_dossier_id": item.source_dry_admission_dossier_id,
        "source_acceptance_seal_id": item.source_acceptance_seal_id,
        "required_attempt_types": item.required_attempt_types,
        "require_all_attempts_blocked": item.require_all_attempts_blocked,
        "execution_enabled": item.execution_enabled,
        "rehearsal_enabled": item.rehearsal_enabled,
        "paper_mode_rehearsal_enabled": item.paper_mode_rehearsal_enabled,
        "shadow_launch_enabled": item.shadow_launch_enabled,
        "paper_mode_launch_enabled": item.paper_mode_launch_enabled,
        "active_paper_enabled": item.active_paper_enabled,
        "paper_admission_enabled": item.paper_admission_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "config_patch_enabled": item.config_patch_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def rehearsal_replay_result_to_dict(item: RehearsalReplayResult) -> dict:
    return {
        "replay_result_id": item.replay_result_id,
        "created_at_utc": item.created_at_utc,
        "replay_plan_id": item.replay_plan_id,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "outcome": item.outcome.value if hasattr(item.outcome, "value") else item.outcome,
        "replayed_attempt_count": item.replayed_attempt_count,
        "blocked_attempt_count": item.blocked_attempt_count,
        "allowed_attempt_count": item.allowed_attempt_count,
        "missing_event_count": item.missing_event_count,
        "passed": item.passed,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def dry_admission_evidence_freeze_item_to_dict(item: DryAdmissionEvidenceFreezeItem) -> dict:
    return {
        "freeze_item_id": item.freeze_item_id,
        "created_at_utc": item.created_at_utc,
        "evidence_type": item.evidence_type,
        "source_ref_id": item.source_ref_id,
        "source_path": item.source_path,
        "frozen": item.frozen,
        "immutable": item.immutable,
        "available": item.available,
        "fresh": item.fresh,
        "stale": item.stale,
        "item_hash": item.item_hash,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def dry_admission_evidence_freeze_bundle_to_dict(item: DryAdmissionEvidenceFreezeBundle) -> dict:
    return {
        "freeze_id": item.freeze_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "decision": item.decision.value if hasattr(item.decision, "value") else item.decision,
        "candidate_id": item.candidate_id,
        "source_dry_admission_dossier_id": item.source_dry_admission_dossier_id,
        "items": [dry_admission_evidence_freeze_item_to_dict(i) for i in item.items],
        "evidence_refs": item.evidence_refs,
        "freeze_hash": item.freeze_hash,
        "frozen": item.frozen,
        "immutable": item.immutable,
        "freeze_is_metadata_only": item.freeze_is_metadata_only,
        "missing_evidence_count": item.missing_evidence_count,
        "stale_evidence_count": item.stale_evidence_count,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def simulator_gate_rule_to_dict(item: SimulatorGateRule) -> dict:
    return {
        "rule_id": item.rule_id,
        "created_at_utc": item.created_at_utc,
        "rule_name": item.rule_name,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "required": item.required,
        "description": item.description,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def simulator_gate_assertion_to_dict(item: SimulatorGateAssertion) -> dict:
    return {
        "assertion_id": item.assertion_id,
        "created_at_utc": item.created_at_utc,
        "assertion_name": item.assertion_name,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "description": item.description,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def final_local_paper_admission_simulator_gate_to_dict(item: FinalLocalPaperAdmissionSimulatorGate) -> dict:
    return {
        "gate_id": item.gate_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "decision": item.decision.value if hasattr(item.decision, "value") else item.decision,
        "candidate_id": item.candidate_id,
        "source_dry_admission_dossier_review_id": item.source_dry_admission_dossier_review_id,
        "source_dry_admission_dossier_id": item.source_dry_admission_dossier_id,
        "source_acceptance_seal_id": item.source_acceptance_seal_id,
        "source_rehearsal_replay_result_id": item.source_rehearsal_replay_result_id,
        "source_evidence_freeze_id": item.source_evidence_freeze_id,
        "rehearsal_replay_result": rehearsal_replay_result_to_dict(item.rehearsal_replay_result) if item.rehearsal_replay_result else None,
        "evidence_freeze": dry_admission_evidence_freeze_bundle_to_dict(item.evidence_freeze) if item.evidence_freeze else None,
        "rules": [simulator_gate_rule_to_dict(r) for r in item.rules],
        "assertions": [simulator_gate_assertion_to_dict(a) for a in item.assertions],
        "gate_hash": item.gate_hash,
        "sealed": item.sealed,
        "immutable": item.immutable,
        "manual_review_required": item.manual_review_required,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "admission_allowed": item.admission_allowed,
        "transition_allowed": item.transition_allowed,
        "rehearsal_allowed": item.rehearsal_allowed,
        "paper_mode_rehearsal_allowed": item.paper_mode_rehearsal_allowed,
        "shadow_launch_allowed": item.shadow_launch_allowed,
        "paper_mode_launch_allowed": item.paper_mode_launch_allowed,
        "simulator_admission_allowed": item.simulator_admission_allowed,
        "local_paper_simulator_allowed": item.local_paper_simulator_allowed,
        "simulator_gate_passed": item.simulator_gate_passed,
        "dry_admission_dossier_valid": item.dry_admission_dossier_valid,
        "dry_admission_acceptance_seal_valid": item.dry_admission_acceptance_seal_valid,
        "all_writes_blocked": item.all_writes_blocked,
        "order_created": item.order_created,
        "mutation_detected": item.mutation_detected,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "safety_flags": [f.value if hasattr(f, "value") else f for f in item.safety_flags],
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def simulator_gate_audit_entry_to_dict(item: SimulatorGateAuditEntry) -> dict:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "action": item.action,
        "decision": item.decision,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def simulator_gate_full_review_to_dict(item: SimulatorGateFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value if hasattr(item.report_type, "value") else item.report_type,
        "gates": [final_local_paper_admission_simulator_gate_to_dict(g) for g in item.gates],
        "rehearsal_replay_plans": [rehearsal_replay_plan_to_dict(p) for p in item.rehearsal_replay_plans],
        "rehearsal_replay_results": [rehearsal_replay_result_to_dict(r) for r in item.rehearsal_replay_results],
        "rehearsal_replay_items": [rehearsal_replay_item_to_dict(i) for i in item.rehearsal_replay_items],
        "evidence_freezes": [dry_admission_evidence_freeze_bundle_to_dict(f) for f in item.evidence_freezes],
        "rules": [simulator_gate_rule_to_dict(r) for r in item.rules],
        "assertions": [simulator_gate_assertion_to_dict(a) for a in item.assertions],
        "audit_entries": [simulator_gate_audit_entry_to_dict(a) for a in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors
    }

def validate_rehearsal_replay_item(item: RehearsalReplayItem) -> None:
    if not item.blocked and item.decision != RehearsalReplayDecision.UNKNOWN:
        raise RehearsalReplayEngineError("Item is not blocked")

def validate_rehearsal_replay_plan(item: RehearsalReplayPlan) -> None:
    if item.execution_enabled or item.rehearsal_enabled or item.paper_mode_rehearsal_enabled or item.shadow_launch_enabled or item.paper_mode_launch_enabled or item.active_paper_enabled or item.paper_admission_enabled or item.broker_execution_enabled or item.paper_state_mutation_enabled or item.config_patch_enabled or item.telegram_real_send_enabled:
        raise RehearsalReplayEngineError("Execution flags must be false")

def validate_rehearsal_replay_result(item: RehearsalReplayResult) -> None:
    if item.passed and item.allowed_attempt_count > 0:
        raise RehearsalReplayAnalyzerError("Passed but has allowed attempts")

def validate_dry_admission_evidence_freeze_bundle(item: DryAdmissionEvidenceFreezeBundle) -> None:
    if not item.frozen or not item.immutable or not item.freeze_is_metadata_only:
        raise DryAdmissionEvidenceFreezeError("Bundle must be frozen, immutable and metadata only")

def validate_simulator_gate_rule(item: SimulatorGateRule) -> None:
    pass

def validate_simulator_gate_assertion(item: SimulatorGateAssertion) -> None:
    pass

def validate_final_local_paper_admission_simulator_gate(item: FinalLocalPaperAdmissionSimulatorGate) -> None:
    if not item.sealed or not item.immutable:
        raise FinalSimulatorGateError("Gate must be sealed and immutable")
    if not item.manual_review_required or not item.activation_denied or not item.all_writes_blocked or not item.simulator_gate_passed:
        raise FinalSimulatorGateError("Gate must require manual review, deny activation, pass simulator and block writes")
    if item.activation_allowed or item.admission_allowed or item.transition_allowed or item.rehearsal_allowed or item.paper_mode_rehearsal_allowed or item.shadow_launch_allowed or item.paper_mode_launch_allowed or item.simulator_admission_allowed or item.local_paper_simulator_allowed or item.order_created or item.mutation_detected:
        raise FinalSimulatorGateError("Gate must not allow execution or mutation")

def validate_simulator_gate_full_review(item: SimulatorGateFullReview) -> None:
    for gate in item.gates:
        validate_final_local_paper_admission_simulator_gate(gate)
