import datetime
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    ReadinessRehearsalStatus, ReadinessRehearsalDecision, StageRehearsalStatus,
    FinalReviewLockStatus, GuardedHandoffStatus, GuardedHandoffDecision,
    ReadinessRehearsalRiskFlag, ReadinessRehearsalReportType
)

@dataclass
class StageRehearsalPlan:
    stage_plan_id: str
    created_at_utc: str
    source_stage: str
    stage_title: str
    status: StageRehearsalStatus
    required_inputs: List[str]
    expected_outputs: List[str]
    execution_enabled: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StageRehearsalResult:
    result_id: str
    created_at_utc: str
    source_stage: str
    status: StageRehearsalStatus
    input_refs: List[str]
    output_refs: List[str]
    safety_flags: List[ReadinessRehearsalRiskFlag]
    passed_safety_checks: bool
    execution_attempted: bool
    active_paper_attempted: bool
    broker_execution_attempted: bool
    paper_state_mutation_attempted: bool
    config_patch_attempted: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessRehearsalRun:
    run_id: str
    created_at_utc: str
    status: ReadinessRehearsalStatus
    source_package_id: Optional[str]
    candidate_id: Optional[str]
    stage_plans: List[StageRehearsalPlan]
    stage_results: List[StageRehearsalResult]
    decision: ReadinessRehearsalDecision
    safety_flags: List[ReadinessRehearsalRiskFlag]
    started_at_utc: Optional[str]
    completed_at_utc: Optional[str]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalReviewLock:
    lock_id: str
    created_at_utc: str
    status: FinalReviewLockStatus
    source_rehearsal_run_id: Optional[str]
    source_package_id: Optional[str]
    candidate_id: Optional[str]
    locked: bool
    lock_reason: str
    lock_hash: Optional[str]
    locked_artifact_refs: List[str]
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GuardedHandoffRegistryEntry:
    handoff_id: str
    created_at_utc: str
    status: GuardedHandoffStatus
    decision: GuardedHandoffDecision
    candidate_id: Optional[str]
    dossier_id: Optional[str]
    board_review_id: Optional[str]
    readiness_package_id: Optional[str]
    rehearsal_run_id: Optional[str]
    final_lock_id: Optional[str]
    evidence_refs: List[str]
    required_followups: List[str]
    safety_flags: List[ReadinessRehearsalRiskFlag]
    manual_review_required: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HandoffEvidenceIndex:
    evidence_index_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    required_evidence_types: List[str]
    available_evidence_types: List[str]
    missing_evidence_types: List[str]
    stale_evidence_types: List[str]
    evidence_refs: List[str]
    evidence_score: Optional[float]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessRehearsalAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[ReadinessRehearsalRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessRehearsalReview:
    review_id: str
    created_at_utc: str
    report_type: ReadinessRehearsalReportType
    rehearsal_runs: List[ReadinessRehearsalRun]
    final_locks: List[FinalReviewLock]
    handoff_entries: List[GuardedHandoffRegistryEntry]
    evidence_indexes: List[HandoffEvidenceIndex]
    audit_entries: List[ReadinessRehearsalAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Functions

def stage_rehearsal_plan_to_dict(item: StageRehearsalPlan) -> dict:
    return asdict(item)

def stage_rehearsal_result_to_dict(item: StageRehearsalResult) -> dict:
    return asdict(item)

def readiness_rehearsal_run_to_dict(item: ReadinessRehearsalRun) -> dict:
    return asdict(item)

def final_review_lock_to_dict(item: FinalReviewLock) -> dict:
    return asdict(item)

def guarded_handoff_registry_entry_to_dict(item: GuardedHandoffRegistryEntry) -> dict:
    return asdict(item)

def handoff_evidence_index_to_dict(item: HandoffEvidenceIndex) -> dict:
    return asdict(item)

def readiness_rehearsal_audit_entry_to_dict(item: ReadinessRehearsalAuditEntry) -> dict:
    return asdict(item)

def readiness_rehearsal_review_to_dict(item: ReadinessRehearsalReview) -> dict:
    return asdict(item)

# ID Generators
def create_stage_rehearsal_plan_id(prefix: str = "stage_rehearsal_plan") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_stage_rehearsal_result_id(prefix: str = "stage_rehearsal_result") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_readiness_rehearsal_run_id(prefix: str = "readiness_rehearsal_run") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_final_review_lock_id(prefix: str = "final_review_lock") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_guarded_handoff_id(prefix: str = "guarded_handoff") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_handoff_evidence_index_id(prefix: str = "handoff_evidence_index") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_readiness_rehearsal_audit_id(prefix: str = "readiness_rehearsal_audit") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def create_readiness_rehearsal_review_id(prefix: str = "readiness_rehearsal_review") -> str:
    return f"{prefix}_{uuid.uuid4()}"

# Validation Functions
def validate_stage_rehearsal_plan(item: StageRehearsalPlan) -> None:
    if item.execution_enabled: raise ValueError("execution_enabled must be False")
    if item.active_paper_enabled: raise ValueError("active_paper_enabled must be False")
    if item.broker_execution_enabled: raise ValueError("broker_execution_enabled must be False")
    if item.paper_state_mutation_enabled: raise ValueError("paper_state_mutation_enabled must be False")
    if item.config_patch_enabled: raise ValueError("config_patch_enabled must be False")

def validate_stage_rehearsal_result(item: StageRehearsalResult) -> None:
    if item.execution_attempted: raise ValueError("execution_attempted must be False")
    if item.active_paper_attempted: raise ValueError("active_paper_attempted must be False")
    if item.broker_execution_attempted: raise ValueError("broker_execution_attempted must be False")
    if item.paper_state_mutation_attempted: raise ValueError("paper_state_mutation_attempted must be False")
    if item.config_patch_attempted: raise ValueError("config_patch_attempted must be False")

def validate_readiness_rehearsal_run(item: ReadinessRehearsalRun) -> None:
    for plan in item.stage_plans:
        validate_stage_rehearsal_plan(plan)
    for result in item.stage_results:
        validate_stage_rehearsal_result(result)

def validate_final_review_lock(item: FinalReviewLock) -> None:
    if item.allows_active_paper: raise ValueError("allows_active_paper must be False")
    if item.allows_broker_execution: raise ValueError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation: raise ValueError("allows_paper_state_mutation must be False")
    if item.allows_config_patch: raise ValueError("allows_config_patch must be False")

def validate_guarded_handoff_registry_entry(item: GuardedHandoffRegistryEntry) -> None:
    if item.allows_active_paper: raise ValueError("allows_active_paper must be False")
    if item.allows_broker_execution: raise ValueError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation: raise ValueError("allows_paper_state_mutation must be False")
    if item.allows_config_patch: raise ValueError("allows_config_patch must be False")

def validate_handoff_evidence_index(item: HandoffEvidenceIndex) -> None:
    if item.evidence_score is not None:
        if not (0 <= item.evidence_score <= 100):
            raise ValueError("evidence_score must be between 0 and 100")

def validate_readiness_rehearsal_review(item: ReadinessRehearsalReview) -> None:
    for run in item.rehearsal_runs:
        validate_readiness_rehearsal_run(run)
    for lock in item.final_locks:
        validate_final_review_lock(lock)
    for entry in item.handoff_entries:
        validate_guarded_handoff_registry_entry(entry)
    for index in item.evidence_indexes:
        validate_handoff_evidence_index(index)
