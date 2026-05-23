from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    PaperModeAdmissionReviewStatus,
    PaperModeAdmissionReviewDecision,
    AdmissionReviewGateStatus,
    LedgerReconciliationStatus,
    LedgerReconciliationDecision,
    NoWriteTransitionCheckpointStatus,
    NoWriteTransitionCheckpointDecision,
    AdmissionEvidenceSealStatus,
    AdmissionReviewRiskFlag,
    AdmissionReviewReportType
)
from usa_signal_bot.core.exceptions import AdmissionReviewValidationError

@dataclass
class AdmissionReviewGate:
    gate_id: str
    created_at_utc: str
    gate_name: str
    status: AdmissionReviewGateStatus
    description: str
    required: bool
    risk_flags: List[AdmissionReviewRiskFlag]
    warnings: List[str]
    errors: List[str]
    observed_value: Optional[Any] = None
    expected_value: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LedgerReconciliationItem:
    item_id: str
    created_at_utc: str
    scope: str
    status: LedgerReconciliationStatus
    expected_acknowledgement: str
    unsafe_note_detected: bool
    activation_language_detected: bool
    risk_flags: List[AdmissionReviewRiskFlag]
    warnings: List[str]
    errors: List[str]
    observed_acknowledgement: Optional[str] = None
    reviewer_id: Optional[str] = None
    note_summary: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LedgerReconciliationReport:
    reconciliation_id: str
    created_at_utc: str
    status: LedgerReconciliationStatus
    decision: LedgerReconciliationDecision
    items: List[LedgerReconciliationItem]
    required_scopes: List[str]
    completed_scopes: List[str]
    missing_scopes: List[str]
    acknowledged_no_write: bool
    acknowledged_not_activation: bool
    activation_allowed: bool
    safety_flags: List[AdmissionReviewRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_ledger_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdmissionEvidenceSeal:
    seal_id: str
    created_at_utc: str
    status: AdmissionEvidenceSealStatus
    evidence_refs: List[str]
    sealed: bool
    immutable: bool
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_review_id: Optional[str] = None
    seal_hash: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalNoWriteTransitionCheckpoint:
    checkpoint_id: str
    created_at_utc: str
    status: NoWriteTransitionCheckpointStatus
    decision: NoWriteTransitionCheckpointDecision
    activation_denied: bool
    activation_allowed: bool
    all_writes_blocked: bool
    mutation_detected: bool
    transition_allowed: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    required_followups: List[str]
    safety_flags: List[AdmissionReviewRiskFlag]
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_admission_review_id: Optional[str] = None
    source_reconciliation_id: Optional[str] = None
    source_evidence_seal_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModeAdmissionReview:
    admission_review_id: str
    created_at_utc: str
    status: PaperModeAdmissionReviewStatus
    decision: PaperModeAdmissionReviewDecision
    gates: List[AdmissionReviewGate]
    evidence_refs: List[str]
    required_followups: List[str]
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    all_writes_blocked: bool
    mutation_detected: bool
    transition_allowed: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: List[AdmissionReviewRiskFlag]
    warnings: List[str]
    errors: List[str]
    candidate_id: Optional[str] = None
    source_dry_admission_review_id: Optional[str] = None
    source_dry_admission_run_id: Optional[str] = None
    source_write_lock_refresh_id: Optional[str] = None
    source_human_ledger_id: Optional[str] = None
    ledger_reconciliation: Optional[LedgerReconciliationReport] = None
    evidence_seal: Optional[AdmissionEvidenceSeal] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdmissionReviewAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[AdmissionReviewRiskFlag]
    warnings: List[str]
    errors: List[str]
    decision: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdmissionReviewFullReport:
    report_id: str
    created_at_utc: str
    report_type: AdmissionReviewReportType
    admission_reviews: List[PaperModeAdmissionReview]
    ledger_reconciliations: List[LedgerReconciliationReport]
    evidence_seals: List[AdmissionEvidenceSeal]
    transition_checkpoints: List[FinalNoWriteTransitionCheckpoint]
    audit_entries: List[AdmissionReviewAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def admission_review_gate_to_dict(item: AdmissionReviewGate) -> dict:
    return {"gate_id": getattr(item, "gate_id", None)}

def ledger_reconciliation_item_to_dict(item: LedgerReconciliationItem) -> dict:
    return {"item_id": getattr(item, "item_id", None)}

def ledger_reconciliation_report_to_dict(item: LedgerReconciliationReport) -> dict:
    return {"reconciliation_id": getattr(item, "reconciliation_id", None)}

def admission_evidence_seal_to_dict(item: AdmissionEvidenceSeal) -> dict:
    return {"seal_id": getattr(item, "seal_id", None)}

def final_no_write_transition_checkpoint_to_dict(item: FinalNoWriteTransitionCheckpoint) -> dict:
    return {"checkpoint_id": getattr(item, "checkpoint_id", None)}

def paper_mode_admission_review_to_dict(item: PaperModeAdmissionReview) -> dict:
    return {"admission_review_id": getattr(item, "admission_review_id", None)}

def admission_review_audit_entry_to_dict(item: AdmissionReviewAuditEntry) -> dict:
    return {"audit_id": getattr(item, "audit_id", None)}

def admission_review_full_report_to_dict(item: AdmissionReviewFullReport) -> dict:
    return {
        "report_id": getattr(item, "report_id", None),
        "created_at_utc": getattr(item, "created_at_utc", None),
        "report_type": getattr(item, "report_type", None)
    }

def validate_admission_review_gate(item: AdmissionReviewGate) -> None:
    pass

def validate_ledger_reconciliation_report(item: LedgerReconciliationReport) -> None:
    if not item.acknowledged_not_activation:
        raise AdmissionReviewValidationError("acknowledged_not_activation must be True")
    if item.activation_allowed:
        raise AdmissionReviewValidationError("activation_allowed must be False")

def validate_admission_evidence_seal(item: AdmissionEvidenceSeal) -> None:
    if item.sealed and not item.immutable:
        raise AdmissionReviewValidationError("If sealed is True, immutable must be True")

def validate_final_no_write_transition_checkpoint(item: FinalNoWriteTransitionCheckpoint) -> None:
    if not item.activation_denied:
        raise AdmissionReviewValidationError("activation_denied must be True")
    if item.activation_allowed:
        raise AdmissionReviewValidationError("activation_allowed must be False")
    if not item.all_writes_blocked:
        raise AdmissionReviewValidationError("all_writes_blocked must be True")
    if item.mutation_detected:
        raise AdmissionReviewValidationError("mutation_detected must be False")
    if item.transition_allowed:
        raise AdmissionReviewValidationError("transition_allowed must be False")
    if item.allows_active_paper:
        raise AdmissionReviewValidationError("allows_active_paper must be False")
    if item.allows_broker_execution:
        raise AdmissionReviewValidationError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation:
        raise AdmissionReviewValidationError("allows_paper_state_mutation must be False")
    if item.allows_config_patch:
        raise AdmissionReviewValidationError("allows_config_patch must be False")
    if item.allows_telegram_real_send:
        raise AdmissionReviewValidationError("allows_telegram_real_send must be False")

def validate_paper_mode_admission_review(item: PaperModeAdmissionReview) -> None:
    if not item.activation_denied:
        raise AdmissionReviewValidationError("activation_denied must be True")
    if item.activation_allowed:
        raise AdmissionReviewValidationError("activation_allowed must be False")
    if not item.all_writes_blocked:
        raise AdmissionReviewValidationError("all_writes_blocked must be True")
    if item.mutation_detected:
        raise AdmissionReviewValidationError("mutation_detected must be False")
    if item.transition_allowed:
        raise AdmissionReviewValidationError("transition_allowed must be False")
    if not item.manual_review_required:
        raise AdmissionReviewValidationError("manual_review_required must be True")
    if item.allows_active_paper:
        raise AdmissionReviewValidationError("allows_active_paper must be False")
    if item.allows_broker_execution:
        raise AdmissionReviewValidationError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation:
        raise AdmissionReviewValidationError("allows_paper_state_mutation must be False")
    if item.allows_config_patch:
        raise AdmissionReviewValidationError("allows_config_patch must be False")
    if item.allows_telegram_real_send:
        raise AdmissionReviewValidationError("allows_telegram_real_send must be False")

def validate_admission_review_full_report(item: AdmissionReviewFullReport) -> None:
    pass

def create_admission_review_gate_id(prefix: str = "admission_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_ledger_reconciliation_item_id(prefix: str = "ledger_reconciliation_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_ledger_reconciliation_id(prefix: str = "ledger_reconciliation") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_admission_evidence_seal_id(prefix: str = "admission_evidence_seal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_transition_checkpoint_id(prefix: str = "no_write_transition_checkpoint") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_admission_review_id(prefix: str = "paper_mode_admission_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_admission_audit_id(prefix: str = "admission_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_admission_full_report_id(prefix: str = "admission_full_report") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# Phase 90 integration stub

# Phase 90 integration
