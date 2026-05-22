import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    FinalHandoffReviewStatus,
    FinalHandoffDecision,
    SealedArchiveStatus,
    ArchiveIntegrityStatus,
    PrePaperCheckpointStatus,
    PrePaperCheckpointDecision,
    PrePaperCheckpointGateStatus,
    FinalHandoffRiskFlag,
    FinalHandoffReportType
)
from usa_signal_bot.core.exceptions import FinalHandoffValidationError

@dataclass
class FinalHandoffEvidenceRef:
    evidence_ref_id: str
    created_at_utc: str
    source_type: str
    source_id: Optional[str]
    source_path: Optional[str]
    required: bool
    available: bool
    stale: bool
    summary: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalHandoffReview:
    handoff_review_id: str
    created_at_utc: str
    status: FinalHandoffReviewStatus
    candidate_id: Optional[str]
    source_handoff_id: Optional[str]
    source_rehearsal_run_id: Optional[str]
    source_final_lock_id: Optional[str]
    evidence_refs: List[FinalHandoffEvidenceRef]
    decision: FinalHandoffDecision
    safety_flags: List[FinalHandoffRiskFlag]
    manual_review_required: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SealedReadinessArchiveManifest:
    archive_id: str
    created_at_utc: str
    status: SealedArchiveStatus
    candidate_id: Optional[str]
    handoff_review_id: Optional[str]
    artifact_refs: List[str]
    evidence_refs: List[str]
    archive_hash: Optional[str]
    sealed: bool
    immutable: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ArchiveIntegrityReport:
    integrity_report_id: str
    created_at_utc: str
    archive_id: Optional[str]
    status: ArchiveIntegrityStatus
    expected_hash: Optional[str]
    observed_hash: Optional[str]
    checked_artifact_count: int
    missing_artifact_count: int
    stale_artifact_count: int
    risk_flags: List[FinalHandoffRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperCheckpointGate:
    gate_id: str
    created_at_utc: str
    gate_name: str
    status: PrePaperCheckpointGateStatus
    observed_value: Optional[Any]
    threshold: Optional[Any]
    description: str
    risk_flags: List[FinalHandoffRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperGovernanceCheckpoint:
    checkpoint_id: str
    created_at_utc: str
    status: PrePaperCheckpointStatus
    candidate_id: Optional[str]
    archive_id: Optional[str]
    handoff_review_id: Optional[str]
    integrity_report_id: Optional[str]
    gates: List[PrePaperCheckpointGate]
    decision: PrePaperCheckpointDecision
    rationale: str
    required_followups: List[str]
    safety_flags: List[FinalHandoffRiskFlag]
    manual_review_required: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalHandoffAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[FinalHandoffRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalHandoffFullReview:
    review_id: str
    created_at_utc: str
    report_type: FinalHandoffReportType
    handoff_reviews: List[FinalHandoffReview]
    archive_manifests: List[SealedReadinessArchiveManifest]
    integrity_reports: List[ArchiveIntegrityReport]
    checkpoints: List[PrePaperGovernanceCheckpoint]
    audit_entries: List[FinalHandoffAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Conversion logic
def final_handoff_evidence_ref_to_dict(item: FinalHandoffEvidenceRef) -> dict:
    return item.__dict__.copy()

def final_handoff_review_to_dict(item: FinalHandoffReview) -> dict:
    d = item.__dict__.copy()
    d['status'] = item.status.value
    d['decision'] = item.decision.value
    d['safety_flags'] = [f.value for f in item.safety_flags]
    d['evidence_refs'] = [final_handoff_evidence_ref_to_dict(e) for e in item.evidence_refs]
    return d

def sealed_readiness_archive_manifest_to_dict(item: SealedReadinessArchiveManifest) -> dict:
    d = item.__dict__.copy()
    d['status'] = item.status.value
    return d

def archive_integrity_report_to_dict(item: ArchiveIntegrityReport) -> dict:
    d = item.__dict__.copy()
    d['status'] = item.status.value
    d['risk_flags'] = [f.value for f in item.risk_flags]
    return d

def pre_paper_checkpoint_gate_to_dict(item: PrePaperCheckpointGate) -> dict:
    d = item.__dict__.copy()
    d['status'] = item.status.value
    d['risk_flags'] = [f.value for f in item.risk_flags]
    return d

def pre_paper_governance_checkpoint_to_dict(item: PrePaperGovernanceCheckpoint) -> dict:
    d = item.__dict__.copy()
    d['status'] = item.status.value
    d['decision'] = item.decision.value
    d['safety_flags'] = [f.value for f in item.safety_flags]
    d['gates'] = [pre_paper_checkpoint_gate_to_dict(g) for g in item.gates]
    return d

def final_handoff_audit_entry_to_dict(item: FinalHandoffAuditEntry) -> dict:
    d = item.__dict__.copy()
    d['risk_flags'] = [f.value for f in item.risk_flags]
    return d

def final_handoff_full_review_to_dict(item: FinalHandoffFullReview) -> dict:
    d = item.__dict__.copy()
    d['report_type'] = item.report_type.value
    d['handoff_reviews'] = [final_handoff_review_to_dict(r) for r in item.handoff_reviews]
    d['archive_manifests'] = [sealed_readiness_archive_manifest_to_dict(m) for m in item.archive_manifests]
    d['integrity_reports'] = [archive_integrity_report_to_dict(r) for r in item.integrity_reports]
    d['checkpoints'] = [pre_paper_governance_checkpoint_to_dict(c) for c in item.checkpoints]
    d['audit_entries'] = [final_handoff_audit_entry_to_dict(a) for a in item.audit_entries]
    return d

# Validation
def _validate_safety_booleans(allows_active_paper: bool, allows_broker_execution: bool, allows_paper_state_mutation: bool, allows_config_patch: bool):
    if allows_active_paper:
        raise FinalHandoffValidationError("allows_active_paper must be False.")
    if allows_broker_execution:
        raise FinalHandoffValidationError("allows_broker_execution must be False.")
    if allows_paper_state_mutation:
        raise FinalHandoffValidationError("allows_paper_state_mutation must be False.")
    if allows_config_patch:
        raise FinalHandoffValidationError("allows_config_patch must be False.")

def validate_final_handoff_review(item: FinalHandoffReview) -> None:
    _validate_safety_booleans(item.allows_active_paper, item.allows_broker_execution, item.allows_paper_state_mutation, item.allows_config_patch)

def validate_sealed_readiness_archive_manifest(item: SealedReadinessArchiveManifest) -> None:
    _validate_safety_booleans(item.allows_active_paper, item.allows_broker_execution, item.allows_paper_state_mutation, item.allows_config_patch)
    if item.sealed and not item.immutable:
        raise FinalHandoffValidationError("Archive manifest sealed is True but immutable is False.")

def validate_archive_integrity_report(item: ArchiveIntegrityReport) -> None:
    pass

def validate_pre_paper_governance_checkpoint(item: PrePaperGovernanceCheckpoint) -> None:
    _validate_safety_booleans(item.allows_active_paper, item.allows_broker_execution, item.allows_paper_state_mutation, item.allows_config_patch)

def validate_final_handoff_full_review(item: FinalHandoffFullReview) -> None:
    for review in item.handoff_reviews:
        validate_final_handoff_review(review)
    for manifest in item.archive_manifests:
        validate_sealed_readiness_archive_manifest(manifest)
    for checkpoint in item.checkpoints:
        validate_pre_paper_governance_checkpoint(checkpoint)

# ID Generators
def _ts(): return datetime.now(timezone.utc).isoformat()
def create_final_handoff_evidence_ref_id(prefix: str = "final_handoff_evidence") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_final_handoff_review_id(prefix: str = "final_handoff_review") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_sealed_archive_id(prefix: str = "sealed_readiness_archive") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_archive_integrity_report_id(prefix: str = "archive_integrity") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_pre_paper_checkpoint_gate_id(prefix: str = "pre_paper_gate") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_pre_paper_checkpoint_id(prefix: str = "pre_paper_checkpoint") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_final_handoff_audit_id(prefix: str = "final_handoff_audit") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_final_handoff_full_review_id(prefix: str = "final_handoff_full_review") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
