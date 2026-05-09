from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime
from usa_signal_bot.core.enums import RollbackSourceType, RollbackPlanStatus, RollbackStepStatus, RollbackSafetyStatus
from usa_signal_bot.core.exceptions import RollbackSourceError

@dataclass
class RollbackSource:
    source_id: str
    source_type: RollbackSourceType
    path: str
    created_at_utc: str | None
    checksum: str | None
    valid: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class RollbackStep:
    step_id: str
    name: str
    source_path: str
    target_path: str
    status: RollbackStepStatus
    action: str
    dry_run: bool
    protected: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class RollbackPlan:
    plan_id: str
    created_at_utc: str
    status: RollbackPlanStatus
    source: RollbackSource
    dry_run: bool
    steps: list[RollbackStep]
    safety_status: RollbackSafetyStatus
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class RollbackExecutionResult:
    execution_id: str
    created_at_utc: str
    status: RollbackPlanStatus
    dry_run: bool
    plan: RollbackPlan
    executed_steps: list[RollbackStep]
    skipped_steps: list[RollbackStep]
    failed_steps: list[RollbackStep]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_rollback_source_id(path: str) -> str:
    import hashlib
    return f"src_{hashlib.md5(path.encode('utf-8')).hexdigest()[:8]}"

def create_rollback_step_id(name: str) -> str:
    return f"step_{uuid.uuid4().hex[:6]}"

def create_rollback_plan_id(prefix: str = "rollback_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rollback_execution_id(prefix: str = "rollback_exec") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_rollback_source(source: RollbackSource) -> None:
    if not source.path:
        raise RollbackSourceError("Source path cannot be empty")
    if not source.valid:
        pass # warning context

def validate_rollback_plan(plan: RollbackPlan) -> None:
    validate_rollback_source(plan.source)
    for step in plan.steps:
        if not plan.dry_run and step.protected:
             pass # Will be handled by executor logic, plan valid but unsafe

    import json
    p_str = json.dumps(rollback_plan_to_dict(plan)).lower()
    for term in ["live approval", "live trade", "send to broker"]:
        if term in p_str:
             raise RollbackSourceError("Prohibited language in rollback plan")

def rollback_source_to_dict(source: RollbackSource) -> dict:
    return {
        "source_id": source.source_id,
        "source_type": source.source_type.value,
        "path": source.path,
        "created_at_utc": source.created_at_utc,
        "checksum": source.checksum,
        "valid": source.valid,
        "warnings": source.warnings,
        "errors": source.errors
    }

def rollback_step_to_dict(step: RollbackStep) -> dict:
    return {
        "step_id": step.step_id,
        "name": step.name,
        "source_path": step.source_path,
        "target_path": step.target_path,
        "status": step.status.value,
        "action": step.action,
        "dry_run": step.dry_run,
        "protected": step.protected,
        "warnings": step.warnings,
        "errors": step.errors
    }

def rollback_plan_to_dict(plan: RollbackPlan) -> dict:
    return {
        "plan_id": plan.plan_id,
        "created_at_utc": plan.created_at_utc,
        "status": plan.status.value,
        "source": rollback_source_to_dict(plan.source),
        "dry_run": plan.dry_run,
        "steps": [rollback_step_to_dict(s) for s in plan.steps],
        "safety_status": plan.safety_status.value,
        "warnings": plan.warnings,
        "errors": plan.errors
    }

def rollback_execution_result_to_dict(result: RollbackExecutionResult) -> dict:
    return {
        "execution_id": result.execution_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "dry_run": result.dry_run,
        "plan": rollback_plan_to_dict(result.plan),
        "executed_steps": [rollback_step_to_dict(s) for s in result.executed_steps],
        "skipped_steps": [rollback_step_to_dict(s) for s in result.skipped_steps],
        "failed_steps": [rollback_step_to_dict(s) for s in result.failed_steps],
        "warnings": result.warnings,
        "errors": result.errors
    }
