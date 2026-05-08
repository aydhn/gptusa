from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
from usa_signal_bot.core.enums import MaintenanceFrequency, MaintenanceTaskStatus

@dataclass
class MaintenanceTask:
    task_id: str
    name: str
    frequency: MaintenanceFrequency
    description: str
    command: Optional[str]
    required: bool
    safety_note: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MaintenanceTaskResult:
    task_id: str
    name: str
    status: MaintenanceTaskStatus
    checked_at_utc: str
    command: Optional[str]
    summary: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class MaintenancePlan:
    plan_id: str
    created_at_utc: str
    tasks: List[MaintenanceTask]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class MaintenanceRunResult:
    run_id: str
    created_at_utc: str
    frequency: MaintenanceFrequency
    status: MaintenanceTaskStatus
    results: List[MaintenanceTaskResult]
    passed_count: int
    warning_count: int
    failed_count: int
    skipped_count: int
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_maintenance_task_id(name: str) -> str:
    return f"task_{uuid.uuid4().hex[:8]}"

def create_maintenance_plan_id(prefix: str = "maint_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_maintenance_run_id(prefix: str = "maint_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_maintenance_task(task: MaintenanceTask) -> None:
    if not task.name:
        raise ValueError("Task name is required")

def validate_maintenance_plan(plan: MaintenancePlan) -> None:
    for task in plan.tasks:
        validate_maintenance_task(task)

def maintenance_task_to_dict(task: MaintenanceTask) -> dict:
    return {
        "task_id": task.task_id,
        "name": task.name,
        "frequency": task.frequency.value,
        "description": task.description,
        "command": task.command,
        "required": task.required,
        "safety_note": task.safety_note,
        "metadata": task.metadata
    }

def maintenance_task_result_to_dict(result: MaintenanceTaskResult) -> dict:
    return {
        "task_id": result.task_id,
        "name": result.name,
        "status": result.status.value,
        "checked_at_utc": result.checked_at_utc,
        "command": result.command,
        "summary": result.summary,
        "warnings": result.warnings,
        "errors": result.errors
    }

def maintenance_plan_to_dict(plan: MaintenancePlan) -> dict:
    return {
        "plan_id": plan.plan_id,
        "created_at_utc": plan.created_at_utc,
        "tasks": [maintenance_task_to_dict(t) for t in plan.tasks],
        "warnings": plan.warnings,
        "errors": plan.errors
    }

def maintenance_run_result_to_dict(result: MaintenanceRunResult) -> dict:
    return {
        "run_id": result.run_id,
        "created_at_utc": result.created_at_utc,
        "frequency": result.frequency.value,
        "status": result.status.value,
        "results": [maintenance_task_result_to_dict(r) for r in result.results],
        "passed_count": result.passed_count,
        "warning_count": result.warning_count,
        "failed_count": result.failed_count,
        "skipped_count": result.skipped_count,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }
