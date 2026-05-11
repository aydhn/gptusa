from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from usa_signal_bot.core.enums import (
    RunLockStatus,
    RunLockScope,
    LockAcquisitionMode,
    ConcurrencyDecision,
    ConcurrencyPolicyStatus,
    SchedulerJobType,
    SchedulerJobStatus,
    SchedulerPlanStatus,
    IdempotencyStatus,
    AtomicWriteStatus,
    SchedulerReportType
)
from datetime import datetime, timezone

@dataclass
class RunIdentity:
    run_id: str
    run_type: RunLockScope
    owner: str
    hostname: str
    process_id: Optional[int]
    created_at_utc: str
    idempotency_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RunLock:
    lock_id: str
    scope: RunLockScope
    lock_path: str
    status: RunLockStatus
    owner: RunIdentity
    acquired_at_utc: Optional[str]
    heartbeat_at_utc: Optional[str]
    expires_at_utc: Optional[str]
    stale_after_seconds: int
    message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LockAcquisitionResult:
    result_id: str
    created_at_utc: str
    status: RunLockStatus
    scope: RunLockScope
    acquired: bool
    lock: Optional[RunLock]
    existing_lock: Optional[RunLock]
    mode: LockAcquisitionMode
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class ConcurrencyPolicy:
    policy_id: str
    scope: RunLockScope
    enabled: bool
    max_concurrent_runs: int
    allow_overlap: bool
    stale_after_seconds: int
    wait_timeout_seconds: int
    acquisition_mode: LockAcquisitionMode
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConcurrencyDecisionResult:
    decision_id: str
    created_at_utc: str
    scope: RunLockScope
    decision: ConcurrencyDecision
    policy: ConcurrencyPolicy
    active_locks: List[RunLock]
    reason: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class IdempotencyRecord:
    key: str
    run_id: str
    scope: RunLockScope
    status: IdempotencyStatus
    created_at_utc: str
    completed_at_utc: Optional[str] = None
    payload_checksum: Optional[str] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SchedulerJob:
    job_id: str
    job_type: SchedulerJobType
    name: str
    command: Optional[str]
    scope: RunLockScope
    enabled: bool
    status: SchedulerJobStatus
    dry_run: bool
    depends_on: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SchedulerPlan:
    plan_id: str
    created_at_utc: str
    status: SchedulerPlanStatus
    dry_run: bool
    jobs: List[SchedulerJob]
    concurrency_decisions: List[ConcurrencyDecisionResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class SchedulerRunResult:
    run_id: str
    created_at_utc: str
    status: SchedulerPlanStatus
    plan: SchedulerPlan
    executed_jobs: List[SchedulerJob] = field(default_factory=list)
    skipped_jobs: List[SchedulerJob] = field(default_factory=list)
    failed_jobs: List[SchedulerJob] = field(default_factory=list)
    lock_results: List[LockAcquisitionResult] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

import uuid

def create_run_id(prefix: str = "run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_lock_id(scope: RunLockScope) -> str:
    return f"lock_{scope.value.lower()}_{uuid.uuid4().hex[:8]}"

def create_lock_acquisition_result_id(prefix: str = "lock_acq") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_concurrency_policy_id(scope: RunLockScope) -> str:
    return f"policy_{scope.value.lower()}"

def create_concurrency_decision_id(prefix: str = "concurrency") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_scheduler_job_id(name: str) -> str:
    safe_name = "".join(c if c.isalnum() else "_" for c in name.lower())
    return f"job_{safe_name}_{uuid.uuid4().hex[:6]}"

def create_scheduler_plan_id(prefix: str = "sched_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_scheduler_run_id(prefix: str = "sched_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# Conversion functions
def run_identity_to_dict(identity: RunIdentity) -> dict:
    run_type_val = identity.run_type.value if hasattr(identity.run_type, "value") else identity.run_type
    return {
        "run_id": identity.run_id,
        "run_type": run_type_val,
        "owner": identity.owner,
        "hostname": identity.hostname,
        "process_id": identity.process_id,
        "created_at_utc": identity.created_at_utc,
        "idempotency_key": identity.idempotency_key,
        "metadata": identity.metadata
    }

def run_lock_to_dict(lock: RunLock) -> dict:
    return {
        "lock_id": lock.lock_id,
        "scope": lock.scope.value,
        "lock_path": lock.lock_path,
        "status": lock.status.value,
        "owner": run_identity_to_dict(lock.owner),
        "acquired_at_utc": lock.acquired_at_utc,
        "heartbeat_at_utc": lock.heartbeat_at_utc,
        "expires_at_utc": lock.expires_at_utc,
        "stale_after_seconds": lock.stale_after_seconds,
        "message": lock.message,
        "metadata": lock.metadata
    }

def lock_acquisition_result_to_dict(result: LockAcquisitionResult) -> dict:
    return {
        "result_id": result.result_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "scope": result.scope.value,
        "acquired": result.acquired,
        "lock": run_lock_to_dict(result.lock) if result.lock else None,
        "existing_lock": run_lock_to_dict(result.existing_lock) if result.existing_lock else None,
        "mode": result.mode.value,
        "warnings": result.warnings,
        "errors": result.errors
    }

def concurrency_policy_to_dict(policy: ConcurrencyPolicy) -> dict:
    return {
        "policy_id": policy.policy_id,
        "scope": policy.scope.value,
        "enabled": policy.enabled,
        "max_concurrent_runs": policy.max_concurrent_runs,
        "allow_overlap": policy.allow_overlap,
        "stale_after_seconds": policy.stale_after_seconds,
        "wait_timeout_seconds": policy.wait_timeout_seconds,
        "acquisition_mode": policy.acquisition_mode.value,
        "description": policy.description,
        "metadata": policy.metadata
    }

def concurrency_decision_result_to_dict(result: ConcurrencyDecisionResult) -> dict:
    return {
        "decision_id": result.decision_id,
        "created_at_utc": result.created_at_utc,
        "scope": result.scope.value,
        "decision": result.decision.value,
        "policy": concurrency_policy_to_dict(result.policy),
        "active_locks": [run_lock_to_dict(l) for l in result.active_locks],
        "reason": result.reason,
        "warnings": result.warnings,
        "errors": result.errors
    }

def idempotency_record_to_dict(record: IdempotencyRecord) -> dict:
    return {
        "key": record.key,
        "run_id": record.run_id,
        "scope": record.scope.value,
        "status": record.status.value,
        "created_at_utc": record.created_at_utc,
        "completed_at_utc": record.completed_at_utc,
        "payload_checksum": record.payload_checksum,
        "output_paths": record.output_paths,
        "metadata": record.metadata
    }

def scheduler_job_to_dict(job: SchedulerJob) -> dict:
    return {
        "job_id": job.job_id,
        "job_type": job.job_type.value,
        "name": job.name,
        "command": job.command,
        "scope": job.scope.value,
        "enabled": job.enabled,
        "status": job.status.value,
        "dry_run": job.dry_run,
        "depends_on": job.depends_on,
        "metadata": job.metadata
    }

def scheduler_plan_to_dict(plan: SchedulerPlan) -> dict:
    return {
        "plan_id": plan.plan_id,
        "created_at_utc": plan.created_at_utc,
        "status": plan.status.value,
        "dry_run": plan.dry_run,
        "jobs": [scheduler_job_to_dict(j) for j in plan.jobs],
        "concurrency_decisions": [concurrency_decision_result_to_dict(d) for d in plan.concurrency_decisions],
        "warnings": plan.warnings,
        "errors": plan.errors
    }

def scheduler_run_result_to_dict(result: SchedulerRunResult) -> dict:
    return {
        "run_id": result.run_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "plan": scheduler_plan_to_dict(result.plan),
        "executed_jobs": [scheduler_job_to_dict(j) for j in result.executed_jobs],
        "skipped_jobs": [scheduler_job_to_dict(j) for j in result.skipped_jobs],
        "failed_jobs": [scheduler_job_to_dict(j) for j in result.failed_jobs],
        "lock_results": [lock_acquisition_result_to_dict(r) for r in result.lock_results],
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

# Validation functions
from usa_signal_bot.core.exceptions import SchedulerValidationError

def validate_run_identity(identity: RunIdentity) -> None:
    if not identity.owner:
        raise SchedulerValidationError("RunIdentity owner cannot be empty")

def validate_run_lock(lock: RunLock) -> None:
    if not lock.lock_path:
        raise SchedulerValidationError("RunLock lock_path cannot be empty")
    if lock.stale_after_seconds <= 0:
        raise SchedulerValidationError("RunLock stale_after_seconds must be positive")
    validate_run_identity(lock.owner)

def validate_concurrency_policy(policy: ConcurrencyPolicy) -> None:
    if policy.max_concurrent_runs <= 0:
        raise SchedulerValidationError("ConcurrencyPolicy max_concurrent_runs must be positive")
    if policy.wait_timeout_seconds < 0:
        raise SchedulerValidationError("ConcurrencyPolicy wait_timeout_seconds cannot be negative")

def validate_scheduler_job(job: SchedulerJob) -> None:
    if job.command:
        # crude check, real validation in scheduler_validation.py
        lower_cmd = job.command.lower()
        if "secret" in lower_cmd or "token" in lower_cmd or "key=" in lower_cmd:
            raise SchedulerValidationError("Command contains secret/token")
        if "broker" in lower_cmd or "live-order" in lower_cmd:
            raise SchedulerValidationError("Scheduler job should not produce broker orders")

def validate_scheduler_plan(plan: SchedulerPlan) -> None:
    for job in plan.jobs:
        validate_scheduler_job(job)
