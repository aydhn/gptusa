from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from usa_signal_bot.core.enums import (
    RuntimeRouteReplayDecision,
    RuntimeMapReplayStatus,
    RuntimeMapReplayOutcome,
    NonExecutionSealIntegrityStatus,
    NonExecutionSealIntegrityDecision,
    PaperReadinessNonExecutionBoardStatus,
    PaperReadinessNonExecutionBoardDecision,
    NonExecutionBoardGateStatus,
    NonExecutionBoardAssertionStatus,
    NonExecutionBoardRiskFlag,
    NonExecutionBoardReportType
)
import uuid
import datetime

def _now_utc_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class RuntimeRouteReplayItem:
    replay_item_id: str
    created_at_utc: str
    route_name: str
    source_component: Optional[str]
    target_component: Optional[str]
    permission: Optional[str]
    decision: RuntimeRouteReplayDecision
    blocked: bool
    read_only: bool
    preview_only: bool
    dry_run_only: bool
    write_allowed: bool
    order_allowed: bool
    broker_allowed: bool
    config_patch_allowed: bool
    telegram_real_send_allowed: bool
    activation_allowed: bool
    paper_admission_allowed: bool
    risk_flags: List[NonExecutionBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeMapReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    source_runtime_map_id: Optional[str]
    source_dossier_id: Optional[str]
    required_component_names: List[str]
    required_route_names: List[str]
    require_all_dangerous_routes_denied: bool
    allow_read_only_routes: bool
    allow_preview_routes: bool
    allow_dry_run_routes: bool
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
class RuntimeMapReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: Optional[str]
    status: RuntimeMapReplayStatus
    outcome: RuntimeMapReplayOutcome
    replayed_route_count: int
    safe_metadata_route_count: int
    dangerous_denied_count: int
    dangerous_allowed_count: int
    missing_component_count: int
    missing_route_count: int
    passed: bool
    risk_flags: List[NonExecutionBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionSealIntegrityItem:
    integrity_item_id: str
    created_at_utc: str
    field_name: str
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    matched: bool
    required: bool
    risk_flags: List[NonExecutionBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionSealIntegrityAudit:
    audit_id: str
    created_at_utc: str
    status: NonExecutionSealIntegrityStatus
    decision: NonExecutionSealIntegrityDecision
    candidate_id: Optional[str]
    source_seal_id: Optional[str]
    source_dossier_id: Optional[str]
    expected_seal_hash: Optional[str]
    observed_seal_hash: Optional[str]
    seal_hash_matches: bool
    items: List[NonExecutionSealIntegrityItem]
    checked_item_count: int
    failed_item_count: int
    missing_boundary_count: int
    confirmed_non_execution: bool
    confirmed_no_broker: bool
    confirmed_no_active_paper: bool
    confirmed_no_paper_admission: bool
    confirmed_no_order: bool
    confirmed_no_write: bool
    confirmed_no_telegram_real_send: bool
    confirmed_no_config_patch: bool
    seal_is_metadata_only: bool
    integrity_valid: bool
    risk_flags: List[NonExecutionBoardRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionBoardGate:
    gate_id: str
    created_at_utc: str
    gate_name: str
    status: NonExecutionBoardGateStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    required: bool
    description: str
    risk_flags: List[NonExecutionBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionBoardAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: NonExecutionBoardAssertionStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    description: str
    risk_flags: List[NonExecutionBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperReadinessNonExecutionBoard:
    board_id: str
    created_at_utc: str
    status: PaperReadinessNonExecutionBoardStatus
    decision: PaperReadinessNonExecutionBoardDecision
    candidate_id: Optional[str]
    source_paper_safe_dossier_review_id: Optional[str]
    source_paper_safe_dossier_id: Optional[str]
    source_runtime_map_id: Optional[str]
    source_non_execution_seal_id: Optional[str]
    runtime_replay_result: Optional[RuntimeMapReplayResult]
    seal_integrity_audit: Optional[NonExecutionSealIntegrityAudit]
    gates: List[NonExecutionBoardGate]
    assertions: List[NonExecutionBoardAssertion]
    board_hash: Optional[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    paper_safe_dossier_valid: bool
    non_execution_confirmed: bool
    runtime_map_safe: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: List[NonExecutionBoardRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionBoardAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[NonExecutionBoardRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionBoardFullReview:
    review_id: str
    created_at_utc: str
    report_type: NonExecutionBoardReportType
    boards: List[PaperReadinessNonExecutionBoard]
    runtime_replay_plans: List[RuntimeMapReplayPlan]
    runtime_replay_results: List[RuntimeMapReplayResult]
    runtime_route_replay_items: List[RuntimeRouteReplayItem]
    seal_integrity_audits: List[NonExecutionSealIntegrityAudit]
    gates: List[NonExecutionBoardGate]
    assertions: List[NonExecutionBoardAssertion]
    audit_entries: List[NonExecutionBoardAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Helpers for ID creation
def create_runtime_route_replay_item_id(prefix: str = "runtime_route_replay") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_runtime_map_replay_plan_id(prefix: str = "runtime_map_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_runtime_map_replay_result_id(prefix: str = "runtime_map_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_seal_integrity_item_id(prefix: str = "seal_integrity_item") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_seal_integrity_audit_id(prefix: str = "seal_integrity_audit") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_non_execution_board_gate_id(prefix: str = "non_execution_board_gate") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_non_execution_board_assertion_id(prefix: str = "non_execution_board_assertion") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_non_execution_board_id(prefix: str = "paper_readiness_non_execution_board") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_non_execution_board_audit_id(prefix: str = "non_execution_board_audit") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_non_execution_board_full_review_id(prefix: str = "non_execution_board_full_review") -> str:
    return f"{prefix}_{uuid.uuid4()}"

# To-Dict Functions
def runtime_route_replay_item_to_dict(item: RuntimeRouteReplayItem) -> dict:
    return {
        "replay_item_id": item.replay_item_id,
        "created_at_utc": item.created_at_utc,
        "route_name": item.route_name,
        "source_component": item.source_component,
        "target_component": item.target_component,
        "permission": item.permission,
        "decision": item.decision.value,
        "blocked": item.blocked,
        "read_only": item.read_only,
        "preview_only": item.preview_only,
        "dry_run_only": item.dry_run_only,
        "write_allowed": item.write_allowed,
        "order_allowed": item.order_allowed,
        "broker_allowed": item.broker_allowed,
        "config_patch_allowed": item.config_patch_allowed,
        "telegram_real_send_allowed": item.telegram_real_send_allowed,
        "activation_allowed": item.activation_allowed,
        "paper_admission_allowed": item.paper_admission_allowed,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def runtime_map_replay_plan_to_dict(item: RuntimeMapReplayPlan) -> dict:
    return {
        "replay_plan_id": item.replay_plan_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "source_runtime_map_id": item.source_runtime_map_id,
        "source_dossier_id": item.source_dossier_id,
        "required_component_names": item.required_component_names,
        "required_route_names": item.required_route_names,
        "require_all_dangerous_routes_denied": item.require_all_dangerous_routes_denied,
        "allow_read_only_routes": item.allow_read_only_routes,
        "allow_preview_routes": item.allow_preview_routes,
        "allow_dry_run_routes": item.allow_dry_run_routes,
        "execution_enabled": item.execution_enabled,
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

def runtime_map_replay_result_to_dict(item: RuntimeMapReplayResult) -> dict:
    return {
        "replay_result_id": item.replay_result_id,
        "created_at_utc": item.created_at_utc,
        "replay_plan_id": item.replay_plan_id,
        "status": item.status.value,
        "outcome": item.outcome.value,
        "replayed_route_count": item.replayed_route_count,
        "safe_metadata_route_count": item.safe_metadata_route_count,
        "dangerous_denied_count": item.dangerous_denied_count,
        "dangerous_allowed_count": item.dangerous_allowed_count,
        "missing_component_count": item.missing_component_count,
        "missing_route_count": item.missing_route_count,
        "passed": item.passed,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def non_execution_seal_integrity_item_to_dict(item: NonExecutionSealIntegrityItem) -> dict:
    return {
        "integrity_item_id": item.integrity_item_id,
        "created_at_utc": item.created_at_utc,
        "field_name": item.field_name,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "matched": item.matched,
        "required": item.required,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def non_execution_seal_integrity_audit_to_dict(item: NonExecutionSealIntegrityAudit) -> dict:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "source_seal_id": item.source_seal_id,
        "source_dossier_id": item.source_dossier_id,
        "expected_seal_hash": item.expected_seal_hash,
        "observed_seal_hash": item.observed_seal_hash,
        "seal_hash_matches": item.seal_hash_matches,
        "items": [non_execution_seal_integrity_item_to_dict(i) for i in item.items],
        "checked_item_count": item.checked_item_count,
        "failed_item_count": item.failed_item_count,
        "missing_boundary_count": item.missing_boundary_count,
        "confirmed_non_execution": item.confirmed_non_execution,
        "confirmed_no_broker": item.confirmed_no_broker,
        "confirmed_no_active_paper": item.confirmed_no_active_paper,
        "confirmed_no_paper_admission": item.confirmed_no_paper_admission,
        "confirmed_no_order": item.confirmed_no_order,
        "confirmed_no_write": item.confirmed_no_write,
        "confirmed_no_telegram_real_send": item.confirmed_no_telegram_real_send,
        "confirmed_no_config_patch": item.confirmed_no_config_patch,
        "seal_is_metadata_only": item.seal_is_metadata_only,
        "integrity_valid": item.integrity_valid,
        "risk_flags": [f.value for f in item.risk_flags],
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def non_execution_board_gate_to_dict(item: NonExecutionBoardGate) -> dict:
    return {
        "gate_id": item.gate_id,
        "created_at_utc": item.created_at_utc,
        "gate_name": item.gate_name,
        "status": item.status.value,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "required": item.required,
        "description": item.description,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def non_execution_board_assertion_to_dict(item: NonExecutionBoardAssertion) -> dict:
    return {
        "assertion_id": item.assertion_id,
        "created_at_utc": item.created_at_utc,
        "assertion_name": item.assertion_name,
        "status": item.status.value,
        "expected_value": item.expected_value,
        "observed_value": item.observed_value,
        "description": item.description,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def paper_readiness_non_execution_board_to_dict(item: PaperReadinessNonExecutionBoard) -> dict:
    return {
        "board_id": item.board_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "source_paper_safe_dossier_review_id": item.source_paper_safe_dossier_review_id,
        "source_paper_safe_dossier_id": item.source_paper_safe_dossier_id,
        "source_runtime_map_id": item.source_runtime_map_id,
        "source_non_execution_seal_id": item.source_non_execution_seal_id,
        "runtime_replay_result": runtime_map_replay_result_to_dict(item.runtime_replay_result) if item.runtime_replay_result else None,
        "seal_integrity_audit": non_execution_seal_integrity_audit_to_dict(item.seal_integrity_audit) if item.seal_integrity_audit else None,
        "gates": [non_execution_board_gate_to_dict(g) for g in item.gates],
        "assertions": [non_execution_board_assertion_to_dict(a) for a in item.assertions],
        "board_hash": item.board_hash,
        "sealed": item.sealed,
        "immutable": item.immutable,
        "manual_review_required": item.manual_review_required,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "admission_allowed": item.admission_allowed,
        "transition_allowed": item.transition_allowed,
        "paper_safe_dossier_valid": item.paper_safe_dossier_valid,
        "non_execution_confirmed": item.non_execution_confirmed,
        "runtime_map_safe": item.runtime_map_safe,
        "all_writes_blocked": item.all_writes_blocked,
        "order_created": item.order_created,
        "mutation_detected": item.mutation_detected,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "safety_flags": [f.value for f in item.safety_flags],
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata
    }

def non_execution_board_audit_entry_to_dict(item: NonExecutionBoardAuditEntry) -> dict:
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
        "metadata": item.metadata
    }

def non_execution_board_full_review_to_dict(item: NonExecutionBoardFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "boards": [paper_readiness_non_execution_board_to_dict(b) for b in item.boards],
        "runtime_replay_plans": [runtime_map_replay_plan_to_dict(p) for p in item.runtime_replay_plans],
        "runtime_replay_results": [runtime_map_replay_result_to_dict(r) for r in item.runtime_replay_results],
        "runtime_route_replay_items": [runtime_route_replay_item_to_dict(i) for i in item.runtime_route_replay_items],
        "seal_integrity_audits": [non_execution_seal_integrity_audit_to_dict(s) for s in item.seal_integrity_audits],
        "gates": [non_execution_board_gate_to_dict(g) for g in item.gates],
        "assertions": [non_execution_board_assertion_to_dict(a) for a in item.assertions],
        "audit_entries": [non_execution_board_audit_entry_to_dict(e) for e in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors
    }

# Validation Functions
from usa_signal_bot.core.exceptions import NonExecutionBoardValidationError

def validate_runtime_route_replay_item(item: RuntimeRouteReplayItem) -> None:
    pass

def validate_runtime_map_replay_plan(item: RuntimeMapReplayPlan) -> None:
    if item.execution_enabled: raise NonExecutionBoardValidationError("execution_enabled must be false")
    if item.active_paper_enabled: raise NonExecutionBoardValidationError("active_paper_enabled must be false")
    if item.paper_admission_enabled: raise NonExecutionBoardValidationError("paper_admission_enabled must be false")
    if item.broker_execution_enabled: raise NonExecutionBoardValidationError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled: raise NonExecutionBoardValidationError("paper_state_mutation_enabled must be false")
    if item.config_patch_enabled: raise NonExecutionBoardValidationError("config_patch_enabled must be false")
    if item.telegram_real_send_enabled: raise NonExecutionBoardValidationError("telegram_real_send_enabled must be false")

def validate_runtime_map_replay_result(item: RuntimeMapReplayResult) -> None:
    if item.passed and item.dangerous_allowed_count > 0:
        raise NonExecutionBoardValidationError("dangerous_allowed_count must be 0 if passed is true")

def validate_non_execution_seal_integrity_audit(item: NonExecutionSealIntegrityAudit) -> None:
    if item.integrity_valid:
        if item.failed_item_count > 0:
            raise NonExecutionBoardValidationError("failed_item_count must be 0 if integrity_valid is true")
        if not item.seal_hash_matches:
            raise NonExecutionBoardValidationError("seal_hash_matches must be true if integrity_valid is true")

def validate_non_execution_board_gate(item: NonExecutionBoardGate) -> None:
    pass

def validate_non_execution_board_assertion(item: NonExecutionBoardAssertion) -> None:
    pass

def validate_paper_readiness_non_execution_board(item: PaperReadinessNonExecutionBoard) -> None:
    if item.sealed and not item.immutable:
        raise NonExecutionBoardValidationError("immutable must be true if sealed is true")
    if not item.manual_review_required:
        raise NonExecutionBoardValidationError("manual_review_required must be true")
    if not item.activation_denied:
        raise NonExecutionBoardValidationError("activation_denied must be true")
    if item.activation_allowed:
        raise NonExecutionBoardValidationError("activation_allowed must be false")
    if item.admission_allowed:
        raise NonExecutionBoardValidationError("admission_allowed must be false")
    if item.transition_allowed:
        raise NonExecutionBoardValidationError("transition_allowed must be false")
    if not item.paper_safe_dossier_valid:
        raise NonExecutionBoardValidationError("paper_safe_dossier_valid must be true")
    if not item.non_execution_confirmed:
        raise NonExecutionBoardValidationError("non_execution_confirmed must be true")
    if not item.runtime_map_safe:
        raise NonExecutionBoardValidationError("runtime_map_safe must be true")
    if not item.all_writes_blocked:
        raise NonExecutionBoardValidationError("all_writes_blocked must be true")
    if item.order_created:
        raise NonExecutionBoardValidationError("order_created must be false")
    if item.mutation_detected:
        raise NonExecutionBoardValidationError("mutation_detected must be false")
    if item.allows_active_paper:
        raise NonExecutionBoardValidationError("allows_active_paper must be false")
    if item.allows_broker_execution:
        raise NonExecutionBoardValidationError("allows_broker_execution must be false")
    if item.allows_paper_state_mutation:
        raise NonExecutionBoardValidationError("allows_paper_state_mutation must be false")
    if item.allows_config_patch:
        raise NonExecutionBoardValidationError("allows_config_patch must be false")
    if item.allows_telegram_real_send:
        raise NonExecutionBoardValidationError("allows_telegram_real_send must be false")

def validate_non_execution_board_full_review(item: NonExecutionBoardFullReview) -> None:
    for b in item.boards:
        validate_paper_readiness_non_execution_board(b)
    for p in item.runtime_replay_plans:
        validate_runtime_map_replay_plan(p)
    for r in item.runtime_replay_results:
        validate_runtime_map_replay_result(r)
    for s in item.seal_integrity_audits:
        validate_non_execution_seal_integrity_audit(s)
