"""Task Queue domain models."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import (
    LocalTaskType, LocalTaskStatus, TaskPriority, TaskQueueStatus,
    ResourcePressure, WorkloadBudgetStatus, TaskConflictType,
    RunWindowStatus, BatchBuildStatus, RunLockScope
)
import uuid
from datetime import datetime, timezone

def create_local_task_id(name: str) -> str:
    return f"task_{uuid.uuid4().hex[:8]}_{name.lower().replace(' ', '_')}"

def create_task_dependency_id(task_id: str, depends_on_task_id: str) -> str:
    return f"dep_{task_id[:6]}_{depends_on_task_id[:6]}"

def create_priority_score_id(task_id: str) -> str:
    return f"pscore_{task_id}"

def create_workload_budget_id(name: str) -> str:
    return f"budget_{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"

def create_workload_evaluation_id(prefix: str = "workload_eval") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_task_conflict_id(task_ids: List[str]) -> str:
    return f"conflict_{uuid.uuid4().hex[:8]}"

def create_task_queue_plan_id(prefix: str = "task_plan") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

def create_task_queue_run_id(prefix: str = "task_run") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

@dataclass
class LocalTask:
    task_id: str
    task_type: LocalTaskType
    name: str
    priority: TaskPriority
    status: LocalTaskStatus
    command: Optional[str]
    lock_scope: RunLockScope
    estimated_duration_seconds: Optional[float]
    estimated_cpu_pct: Optional[float]
    estimated_gpu_pct: Optional[float]
    estimated_ram_mb: Optional[float]
    estimated_disk_mb: Optional[float]
    estimated_network_mb: Optional[float]
    dry_run: bool
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskDependency:
    dependency_id: str
    task_id: str
    depends_on_task_id: str
    required: bool
    reason: Optional[str] = None

@dataclass
class TaskPriorityScore:
    task_id: str
    base_priority: TaskPriority
    score: float
    urgency_score: float
    safety_score: float
    freshness_score: float
    workload_penalty: float
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResourceEstimate:
    task_id: str
    cpu_pct: Optional[float]
    gpu_pct: Optional[float]
    ram_mb: Optional[float]
    disk_mb: Optional[float]
    network_mb: Optional[float]
    duration_seconds: Optional[float]
    pressure: ResourcePressure
    warnings: List[str]
    errors: List[str]

@dataclass
class WorkloadBudget:
    budget_id: str
    name: str
    max_cpu_pct: float
    max_gpu_pct: float
    max_ram_mb: float
    max_disk_mb: float
    max_network_mb_per_run: float
    max_duration_seconds: float
    max_parallel_tasks: int
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkloadBudgetEvaluation:
    evaluation_id: str
    created_at_utc: str
    status: WorkloadBudgetStatus
    budget: WorkloadBudget
    tasks: List[LocalTask]
    total_estimated_cpu_pct: float
    total_estimated_gpu_pct: float
    total_estimated_ram_mb: float
    total_estimated_disk_mb: float
    total_estimated_network_mb: float
    total_estimated_duration_seconds: float
    warnings: List[str]
    errors: List[str]

@dataclass
class TaskConflict:
    conflict_id: str
    conflict_type: TaskConflictType
    task_ids: List[str]
    severity: str
    message: str
    blocking: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskQueuePlan:
    plan_id: str
    created_at_utc: str
    status: TaskQueueStatus
    dry_run: bool
    tasks: List[LocalTask]
    priority_scores: List[TaskPriorityScore]
    budget_evaluation: Optional[WorkloadBudgetEvaluation]
    conflicts: List[TaskConflict]
    planned_batches: List[Dict[str, Any]]
    warnings: List[str]
    errors: List[str]

@dataclass
class TaskQueueRunResult:
    run_id: str
    created_at_utc: str
    status: TaskQueueStatus
    plan: TaskQueuePlan
    executed_tasks: List[LocalTask]
    skipped_tasks: List[LocalTask]
    blocked_tasks: List[LocalTask]
    failed_tasks: List[LocalTask]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def local_task_to_dict(task: LocalTask) -> dict:
    return {
        "task_id": task.task_id,
        "task_type": task.task_type.value,
        "name": task.name,
        "priority": task.priority.value,
        "status": task.status.value,
        "command": task.command,
        "lock_scope": task.lock_scope.value,
        "estimated_duration_seconds": task.estimated_duration_seconds,
        "estimated_cpu_pct": task.estimated_cpu_pct,
        "estimated_gpu_pct": task.estimated_gpu_pct,
        "estimated_ram_mb": task.estimated_ram_mb,
        "estimated_disk_mb": task.estimated_disk_mb,
        "estimated_network_mb": task.estimated_network_mb,
        "dry_run": task.dry_run,
        "dependencies": task.dependencies,
        "metadata": task.metadata
    }

def task_dependency_to_dict(dep: TaskDependency) -> dict:
    return {"dependency_id": dep.dependency_id, "task_id": dep.task_id, "depends_on_task_id": dep.depends_on_task_id, "required": dep.required, "reason": dep.reason}

def task_priority_score_to_dict(score: TaskPriorityScore) -> dict:
    return {"task_id": score.task_id, "base_priority": score.base_priority.value, "score": score.score, "urgency_score": score.urgency_score, "safety_score": score.safety_score, "freshness_score": score.freshness_score, "workload_penalty": score.workload_penalty, "reason": score.reason, "metadata": score.metadata}

def resource_estimate_to_dict(estimate: ResourceEstimate) -> dict:
    return {"task_id": estimate.task_id, "cpu_pct": estimate.cpu_pct, "gpu_pct": estimate.gpu_pct, "ram_mb": estimate.ram_mb, "disk_mb": estimate.disk_mb, "network_mb": estimate.network_mb, "duration_seconds": estimate.duration_seconds, "pressure": estimate.pressure.value, "warnings": estimate.warnings, "errors": estimate.errors}

def workload_budget_to_dict(budget: WorkloadBudget) -> dict:
    return {"budget_id": budget.budget_id, "name": budget.name, "max_cpu_pct": budget.max_cpu_pct, "max_gpu_pct": budget.max_gpu_pct, "max_ram_mb": budget.max_ram_mb, "max_disk_mb": budget.max_disk_mb, "max_network_mb_per_run": budget.max_network_mb_per_run, "max_duration_seconds": budget.max_duration_seconds, "max_parallel_tasks": budget.max_parallel_tasks, "metadata": budget.metadata}

def workload_budget_evaluation_to_dict(evaluation: WorkloadBudgetEvaluation) -> dict:
    return {"evaluation_id": evaluation.evaluation_id, "created_at_utc": evaluation.created_at_utc, "status": evaluation.status.value, "budget": workload_budget_to_dict(evaluation.budget), "tasks": [local_task_to_dict(t) for t in evaluation.tasks], "total_estimated_cpu_pct": evaluation.total_estimated_cpu_pct, "total_estimated_gpu_pct": evaluation.total_estimated_gpu_pct, "total_estimated_ram_mb": evaluation.total_estimated_ram_mb, "total_estimated_disk_mb": evaluation.total_estimated_disk_mb, "total_estimated_network_mb": evaluation.total_estimated_network_mb, "total_estimated_duration_seconds": evaluation.total_estimated_duration_seconds, "warnings": evaluation.warnings, "errors": evaluation.errors}

def task_conflict_to_dict(conflict: TaskConflict) -> dict:
    return {"conflict_id": conflict.conflict_id, "conflict_type": conflict.conflict_type.value, "task_ids": conflict.task_ids, "severity": conflict.severity, "message": conflict.message, "blocking": conflict.blocking, "metadata": conflict.metadata}

def task_queue_plan_to_dict(plan: TaskQueuePlan) -> dict:
    return {"plan_id": plan.plan_id, "created_at_utc": plan.created_at_utc, "status": plan.status.value, "dry_run": plan.dry_run, "tasks": [local_task_to_dict(t) for t in plan.tasks], "priority_scores": [task_priority_score_to_dict(s) for s in plan.priority_scores], "budget_evaluation": workload_budget_evaluation_to_dict(plan.budget_evaluation) if plan.budget_evaluation else None, "conflicts": [task_conflict_to_dict(c) for c in plan.conflicts], "planned_batches": plan.planned_batches, "warnings": plan.warnings, "errors": plan.errors}

def task_queue_run_result_to_dict(result: TaskQueueRunResult) -> dict:
    return {"run_id": result.run_id, "created_at_utc": result.created_at_utc, "status": result.status.value, "plan": task_queue_plan_to_dict(result.plan), "executed_tasks": [local_task_to_dict(t) for t in result.executed_tasks], "skipped_tasks": [local_task_to_dict(t) for t in result.skipped_tasks], "blocked_tasks": [local_task_to_dict(t) for t in result.blocked_tasks], "failed_tasks": [local_task_to_dict(t) for t in result.failed_tasks], "output_paths": result.output_paths, "warnings": result.warnings, "errors": result.errors}

def validate_local_task(task: LocalTask) -> None:
    from usa_signal_bot.core.exceptions import TaskQueueValidationError
    if not task.name:
        raise TaskQueueValidationError("Task name cannot be empty")
    for val in [task.estimated_cpu_pct, task.estimated_gpu_pct, task.estimated_ram_mb, task.estimated_disk_mb, task.estimated_network_mb, task.estimated_duration_seconds]:
        if val is not None and val < 0:
            raise TaskQueueValidationError("Estimated resource values cannot be negative")
    if task.command:
        if "token" in task.command.lower() or "secret" in task.command.lower():
            raise TaskQueueValidationError("Task command must not contain secrets or tokens")
        for w in ["cleanup-execute", "rollback-execute", "live-order", "demo-order", "send-broker-order"]:
            if w in task.command.lower():
                if task.status != LocalTaskStatus.BLOCKED:
                    task.status = LocalTaskStatus.BLOCKED
                    task.metadata["blocked_reason"] = f"Destructive command detected: {w}"

def validate_workload_budget(budget: WorkloadBudget) -> None:
    from usa_signal_bot.core.exceptions import WorkloadBudgetError
    if budget.max_parallel_tasks <= 0:
        raise WorkloadBudgetError("max_parallel_tasks must be positive")

def validate_task_queue_plan(plan: TaskQueuePlan) -> None:
    pass
