from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    PaperModeDryAdmissionStatus,
    PaperModeDryAdmissionDecision,
    DryAdmissionStepStatus,
    WriteLockProofRefreshStatus,
    WriteLockProofRefreshDecision,
    HumanApprovalLedgerStatus,
    HumanApprovalLedgerDecision,
    HumanApprovalEntryStatus,
    HumanApprovalScope,
    DryAdmissionRiskFlag,
    DryAdmissionReportType
)

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class DryAdmissionStep:
    step_id: str
    step_name: str
    created_at_utc: str = field(default_factory=_now_utc)
    status: DryAdmissionStepStatus = DryAdmissionStepStatus.UNKNOWN
    input_refs: List[str] = field(default_factory=list)
    output_refs: List[str] = field(default_factory=list)
    write_attempted: bool = False
    order_attempted: bool = False
    broker_send_attempted: bool = False
    config_patch_attempted: bool = False
    telegram_real_send_attempted: bool = False
    active_paper_enable_attempted: bool = False
    mutation_detected: bool = False
    risk_flags: List[DryAdmissionRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModeDryAdmissionPlan:
    plan_id: str
    created_at_utc: str = field(default_factory=_now_utc)
    candidate_id: Optional[str] = None
    source_no_write_review_id: Optional[str] = None
    source_contract_id: Optional[str] = None
    source_preflight_id: Optional[str] = None
    decision: PaperModeDryAdmissionDecision = PaperModeDryAdmissionDecision.UNKNOWN
    required_inputs: List[str] = field(default_factory=list)
    planned_steps: List[str] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)
    require_write_lock_refresh: bool = True
    require_human_ledger: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeWriteLockProofRefresh:
    refresh_id: str
    created_at_utc: str = field(default_factory=_now_utc)
    status: WriteLockProofRefreshStatus = WriteLockProofRefreshStatus.UNKNOWN
    decision: WriteLockProofRefreshDecision = WriteLockProofRefreshDecision.UNKNOWN
    candidate_id: Optional[str] = None
    source_write_block_proof_id: Optional[str] = None
    source_contract_id: Optional[str] = None
    read_only_snapshot_hash_before: Optional[str] = None
    read_only_snapshot_hash_after: Optional[str] = None
    write_attempt_types_verified: List[str] = field(default_factory=list)
    blocked_write_attempt_count: int = 0
    unblocked_write_attempt_count: int = 0
    all_writes_blocked: bool = True
    hash_unchanged: bool = True
    mutation_detected: bool = False
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_paper_state_mutation: bool = False
    allows_config_patch: bool = False
    allows_telegram_real_send: bool = False
    risk_flags: List[DryAdmissionRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HumanApprovalLedgerEntry:
    ledger_entry_id: str
    scope: HumanApprovalScope
    note: str
    created_at_utc: str = field(default_factory=_now_utc)
    status: HumanApprovalEntryStatus = HumanApprovalEntryStatus.UNKNOWN
    reviewer_id: Optional[str] = None
    candidate_id: Optional[str] = None
    source_review_id: Optional[str] = None
    acknowledged_no_write: bool = True
    acknowledged_not_activation: bool = True
    activation_allowed: bool = False
    requires_followup: bool = False
    followups: List[str] = field(default_factory=list)
    risk_flags: List[DryAdmissionRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HumanApprovalLedger:
    ledger_id: str
    created_at_utc: str = field(default_factory=_now_utc)
    status: HumanApprovalLedgerStatus = HumanApprovalLedgerStatus.UNKNOWN
    decision: HumanApprovalLedgerDecision = HumanApprovalLedgerDecision.UNKNOWN
    candidate_id: Optional[str] = None
    entries: List[HumanApprovalLedgerEntry] = field(default_factory=list)
    required_scopes: List[str] = field(default_factory=list)
    completed_scopes: List[str] = field(default_factory=list)
    missing_scopes: List[str] = field(default_factory=list)
    acknowledged_no_write: bool = True
    acknowledged_not_activation: bool = True
    activation_allowed: bool = False
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_paper_state_mutation: bool = False
    allows_config_patch: bool = False
    allows_telegram_real_send: bool = False
    required_followups: List[str] = field(default_factory=list)
    risk_flags: List[DryAdmissionRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModeDryAdmissionRun:
    run_id: str
    created_at_utc: str = field(default_factory=_now_utc)
    status: PaperModeDryAdmissionStatus = PaperModeDryAdmissionStatus.UNKNOWN
    decision: PaperModeDryAdmissionDecision = PaperModeDryAdmissionDecision.UNKNOWN
    candidate_id: Optional[str] = None
    plan: Optional[PaperModeDryAdmissionPlan] = None
    write_lock_refresh: Optional[RuntimeWriteLockProofRefresh] = None
    human_ledger: Optional[HumanApprovalLedger] = None
    steps: List[DryAdmissionStep] = field(default_factory=list)
    read_only_snapshot_hash: Optional[str] = None
    output_summary: Dict[str, Any] = field(default_factory=dict)
    activation_denied: bool = True
    activation_allowed: bool = False
    all_writes_blocked: bool = True
    mutation_detected: bool = False
    safety_flags: List[DryAdmissionRiskFlag] = field(default_factory=list)
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionAuditEntry:
    audit_id: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    created_at_utc: str = field(default_factory=_now_utc)
    decision: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)
    risk_flags: List[DryAdmissionRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionFullReview:
    review_id: str
    report_type: DryAdmissionReportType
    created_at_utc: str = field(default_factory=_now_utc)
    plans: List[PaperModeDryAdmissionPlan] = field(default_factory=list)
    runs: List[PaperModeDryAdmissionRun] = field(default_factory=list)
    write_lock_refreshes: List[RuntimeWriteLockProofRefresh] = field(default_factory=list)
    human_ledgers: List[HumanApprovalLedger] = field(default_factory=list)
    audit_entries: List[DryAdmissionAuditEntry] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def dry_admission_step_to_dict(item: DryAdmissionStep) -> dict:
    return {
        "step_id": item.step_id,
        "created_at_utc": item.created_at_utc,
        "step_name": item.step_name,
        "status": item.status.value,
        "input_refs": item.input_refs,
        "output_refs": item.output_refs,
        "write_attempted": item.write_attempted,
        "order_attempted": item.order_attempted,
        "broker_send_attempted": item.broker_send_attempted,
        "config_patch_attempted": item.config_patch_attempted,
        "telegram_real_send_attempted": item.telegram_real_send_attempted,
        "active_paper_enable_attempted": item.active_paper_enable_attempted,
        "mutation_detected": item.mutation_detected,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def paper_mode_dry_admission_plan_to_dict(item: PaperModeDryAdmissionPlan) -> dict:
    return {
        "plan_id": item.plan_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "source_no_write_review_id": item.source_no_write_review_id,
        "source_contract_id": item.source_contract_id,
        "source_preflight_id": item.source_preflight_id,
        "decision": item.decision.value,
        "required_inputs": item.required_inputs,
        "planned_steps": item.planned_steps,
        "expected_outputs": item.expected_outputs,
        "require_write_lock_refresh": item.require_write_lock_refresh,
        "require_human_ledger": item.require_human_ledger,
        "execution_enabled": item.execution_enabled,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "config_patch_enabled": item.config_patch_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def runtime_write_lock_proof_refresh_to_dict(item: RuntimeWriteLockProofRefresh) -> dict:
    return {
        "refresh_id": item.refresh_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "source_write_block_proof_id": item.source_write_block_proof_id,
        "source_contract_id": item.source_contract_id,
        "read_only_snapshot_hash_before": item.read_only_snapshot_hash_before,
        "read_only_snapshot_hash_after": item.read_only_snapshot_hash_after,
        "write_attempt_types_verified": item.write_attempt_types_verified,
        "blocked_write_attempt_count": item.blocked_write_attempt_count,
        "unblocked_write_attempt_count": item.unblocked_write_attempt_count,
        "all_writes_blocked": item.all_writes_blocked,
        "hash_unchanged": item.hash_unchanged,
        "mutation_detected": item.mutation_detected,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def human_approval_ledger_entry_to_dict(item: HumanApprovalLedgerEntry) -> dict:
    return {
        "ledger_entry_id": item.ledger_entry_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "scope": item.scope.value,
        "reviewer_id": item.reviewer_id,
        "candidate_id": item.candidate_id,
        "source_review_id": item.source_review_id,
        "note": item.note,
        "acknowledged_no_write": item.acknowledged_no_write,
        "acknowledged_not_activation": item.acknowledged_not_activation,
        "activation_allowed": item.activation_allowed,
        "requires_followup": item.requires_followup,
        "followups": item.followups,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def human_approval_ledger_to_dict(item: HumanApprovalLedger) -> dict:
    return {
        "ledger_id": item.ledger_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "entries": [human_approval_ledger_entry_to_dict(e) for e in item.entries],
        "required_scopes": item.required_scopes,
        "completed_scopes": item.completed_scopes,
        "missing_scopes": item.missing_scopes,
        "acknowledged_no_write": item.acknowledged_no_write,
        "acknowledged_not_activation": item.acknowledged_not_activation,
        "activation_allowed": item.activation_allowed,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "required_followups": item.required_followups,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def paper_mode_dry_admission_run_to_dict(item: PaperModeDryAdmissionRun) -> dict:
    return {
        "run_id": item.run_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "plan": paper_mode_dry_admission_plan_to_dict(item.plan) if item.plan else None,
        "write_lock_refresh": runtime_write_lock_proof_refresh_to_dict(item.write_lock_refresh) if item.write_lock_refresh else None,
        "human_ledger": human_approval_ledger_to_dict(item.human_ledger) if item.human_ledger else None,
        "steps": [dry_admission_step_to_dict(s) for s in item.steps],
        "read_only_snapshot_hash": item.read_only_snapshot_hash,
        "output_summary": item.output_summary,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "all_writes_blocked": item.all_writes_blocked,
        "mutation_detected": item.mutation_detected,
        "safety_flags": [f.value for f in item.safety_flags],
        "started_at_utc": item.started_at_utc,
        "completed_at_utc": item.completed_at_utc,
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_admission_audit_entry_to_dict(item: DryAdmissionAuditEntry) -> dict:
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

def dry_admission_full_review_to_dict(item: DryAdmissionFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "plans": [paper_mode_dry_admission_plan_to_dict(p) for p in item.plans],
        "runs": [paper_mode_dry_admission_run_to_dict(r) for r in item.runs],
        "write_lock_refreshes": [runtime_write_lock_proof_refresh_to_dict(w) for w in item.write_lock_refreshes],
        "human_ledgers": [human_approval_ledger_to_dict(l) for l in item.human_ledgers],
        "audit_entries": [dry_admission_audit_entry_to_dict(a) for a in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_dry_admission_step(item: DryAdmissionStep) -> None:
    if item.write_attempted or item.order_attempted or item.broker_send_attempted or item.config_patch_attempted or item.telegram_real_send_attempted or item.active_paper_enable_attempted or item.mutation_detected:
        raise ValueError("Dry admission step must not perform any write or order attempts.")

def validate_paper_mode_dry_admission_plan(item: PaperModeDryAdmissionPlan) -> None:
    if item.execution_enabled or item.active_paper_enabled or item.broker_execution_enabled or item.paper_state_mutation_enabled or item.config_patch_enabled or item.telegram_real_send_enabled:
        raise ValueError("Plan must not allow any execution, mutation, or real sends.")
    if not item.require_write_lock_refresh or not item.require_human_ledger:
        raise ValueError("Plan must require write-lock refresh and human ledger.")

def validate_runtime_write_lock_proof_refresh(item: RuntimeWriteLockProofRefresh) -> None:
    if not item.all_writes_blocked:
        raise ValueError("Write lock refresh requires all_writes_blocked=True.")
    if item.unblocked_write_attempt_count > 0:
        raise ValueError("unblocked_write_attempt_count must be 0.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Refresh must not allow any execution or mutation.")

def validate_human_approval_ledger_entry(item: HumanApprovalLedgerEntry) -> None:
    if item.activation_allowed:
        raise ValueError("Human approval ledger entry must not allow activation.")
    if not item.acknowledged_not_activation:
        raise ValueError("Entry must acknowledge that it is not an activation approval.")
    safe_note = item.note.lower()
    unsafe_words = ["aktif et", "canlıya al", "emir gönder", "live approved", "sent to broker", "gerçek emir"]
    for word in unsafe_words:
        if word in safe_note:
            raise ValueError(f"Ledger entry note contains unsafe execution language: {word}")

def validate_human_approval_ledger(item: HumanApprovalLedger) -> None:
    if item.activation_allowed:
        raise ValueError("Human approval ledger must not allow activation.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Human ledger must not allow any execution or mutation.")

def validate_paper_mode_dry_admission_run(item: PaperModeDryAdmissionRun) -> None:
    if item.activation_allowed or not item.activation_denied:
        raise ValueError("Run must deny activation.")
    if not item.all_writes_blocked or item.mutation_detected:
        raise ValueError("Run must block all writes and detect no mutation.")

def validate_dry_admission_full_review(item: DryAdmissionFullReview) -> None:
    for p in item.plans: validate_paper_mode_dry_admission_plan(p)
    for r in item.runs: validate_paper_mode_dry_admission_run(r)
    for w in item.write_lock_refreshes: validate_runtime_write_lock_proof_refresh(w)
    for l in item.human_ledgers: validate_human_approval_ledger(l)

def create_dry_admission_step_id(prefix: str = "dry_admission_step") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_plan_id(prefix: str = "dry_admission_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_write_lock_refresh_id(prefix: str = "write_lock_refresh") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_human_approval_ledger_entry_id(prefix: str = "human_ledger_entry") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_human_approval_ledger_id(prefix: str = "human_approval_ledger") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_run_id(prefix: str = "dry_admission_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_audit_id(prefix: str = "dry_admission_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_full_review_id(prefix: str = "dry_admission_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
