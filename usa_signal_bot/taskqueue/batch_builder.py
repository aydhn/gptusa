from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from usa_signal_bot.taskqueue.task_models import LocalTask, WorkloadBudget, WorkloadBudgetEvaluation, TaskConflict
from usa_signal_bot.taskqueue.workload_budget import evaluate_workload_budget
from usa_signal_bot.taskqueue.conflict_detector import detect_task_conflicts
from usa_signal_bot.core.enums import BatchBuildStatus
import uuid
from datetime import datetime, timezone

def create_task_batch_id(prefix: str = "task_batch") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

@dataclass
class TaskBatch:
    batch_id: str
    created_at_utc: str
    status: BatchBuildStatus
    tasks: List[LocalTask]
    total_estimated_duration_seconds: float
    budget_evaluation: Optional[WorkloadBudgetEvaluation]
    conflicts: List[TaskConflict]
    warnings: List[str]
    errors: List[str]

def build_safe_task_batch(tasks: List[LocalTask], budget: Optional[WorkloadBudget] = None, max_tasks: Optional[int] = None) -> TaskBatch:
    max_t = max_tasks if max_tasks else (budget.max_parallel_tasks if budget else len(tasks))
    selected = tasks[:max_t]
    conflicts = detect_task_conflicts(selected, budget)
    blocking = [c for c in conflicts if c.blocking]
    eval = evaluate_workload_budget(selected, budget)
    status = BatchBuildStatus.BLOCKED if blocking else BatchBuildStatus.BUILT
    errors = eval.errors.copy()
    if blocking: errors.append(f"Blocked by {len(blocking)} conflicts")
    return TaskBatch(create_task_batch_id(), datetime.now(timezone.utc).isoformat(), status, selected, sum(t.estimated_duration_seconds or 0 for t in selected), eval, conflicts, eval.warnings.copy(), errors)

def split_tasks_into_batches(tasks: List[LocalTask], budget: Optional[WorkloadBudget] = None) -> List[TaskBatch]:
    if not tasks: return []
    chunk_size = budget.max_parallel_tasks if budget else 1
    return [build_safe_task_batch(tasks[i:i+chunk_size], budget, chunk_size) for i in range(0, len(tasks), chunk_size)]

def task_batch_to_dict(batch: TaskBatch) -> dict:
    from usa_signal_bot.taskqueue.task_models import local_task_to_dict, workload_budget_evaluation_to_dict, task_conflict_to_dict
    return {"batch_id": batch.batch_id, "created_at_utc": batch.created_at_utc, "status": batch.status.value, "tasks": [local_task_to_dict(t) for t in batch.tasks], "total_estimated_duration_seconds": batch.total_estimated_duration_seconds, "budget_evaluation": workload_budget_evaluation_to_dict(batch.budget_evaluation) if batch.budget_evaluation else None, "conflicts": [task_conflict_to_dict(c) for c in batch.conflicts], "warnings": batch.warnings, "errors": batch.errors}

def task_batch_to_text(batch: TaskBatch, limit: int = 50) -> str:
    lines = [f"Task Batch: {batch.batch_id}", f"Status: {batch.status.value} | Tasks: {len(batch.tasks)}", f"Duration: {batch.total_estimated_duration_seconds}s"]
    if batch.errors: lines.append(f"Errors: {len(batch.errors)}")
    return "\n".join(lines)
