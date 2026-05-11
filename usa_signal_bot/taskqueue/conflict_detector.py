from typing import List, Dict
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskConflict, WorkloadBudget, create_task_conflict_id
from usa_signal_bot.core.enums import TaskConflictType

def detect_task_conflicts(tasks: List[LocalTask], budget: WorkloadBudget = None) -> List[TaskConflict]:
    conflicts = detect_lock_scope_conflicts(tasks)
    if budget: conflicts.extend(detect_resource_budget_conflicts(tasks, budget))
    conflicts.extend(detect_duplicate_task_conflicts(tasks))
    conflicts.extend(detect_destructive_task_conflicts(tasks))
    return conflicts

def detect_lock_scope_conflicts(tasks: List[LocalTask]) -> List[TaskConflict]:
    conflicts, scope_map = [], {}
    for t in tasks:
        if t.lock_scope: scope_map.setdefault(t.lock_scope.value, []).append(t)
    for scope, grouped in scope_map.items():
        if len(grouped) > 1 and scope != "GLOBAL":
            task_ids = [t.task_id for t in grouped]
            conflicts.append(TaskConflict(create_task_conflict_id(task_ids), TaskConflictType.LOCK_SCOPE_CONFLICT, task_ids, "WARNING", f"Multiple tasks share lock scope: {scope}", False, {}))
    return conflicts

def detect_resource_budget_conflicts(tasks: List[LocalTask], budget: WorkloadBudget) -> List[TaskConflict]:
    conflicts = []
    for t in tasks:
        if t.estimated_cpu_pct and t.estimated_cpu_pct > budget.max_cpu_pct: conflicts.append(TaskConflict(create_task_conflict_id([t.task_id]), TaskConflictType.RESOURCE_BUDGET_CONFLICT, [t.task_id], "ERROR", "CPU exceeds budget", True, {}))
        if t.estimated_ram_mb and t.estimated_ram_mb > budget.max_ram_mb: conflicts.append(TaskConflict(create_task_conflict_id([t.task_id]), TaskConflictType.RESOURCE_BUDGET_CONFLICT, [t.task_id], "ERROR", "RAM exceeds budget", True, {}))
    return conflicts

def detect_duplicate_task_conflicts(tasks: List[LocalTask]) -> List[TaskConflict]:
    conflicts, type_map = [], {}
    for t in tasks: type_map.setdefault(t.task_type.value, []).append(t)
    for t_type, grouped in type_map.items():
        if len(grouped) > 1:
            task_ids = [t.task_id for t in grouped]
            conflicts.append(TaskConflict(create_task_conflict_id(task_ids), TaskConflictType.DUPLICATE_TASK, task_ids, "WARNING", f"Duplicate tasks for type: {t_type}", False, {}))
    return conflicts

def detect_destructive_task_conflicts(tasks: List[LocalTask]) -> List[TaskConflict]:
    conflicts, destructive = [], ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]
    for t in tasks:
        if t.command and any(w in t.command for w in destructive):
            conflicts.append(TaskConflict(create_task_conflict_id([t.task_id]), TaskConflictType.DESTRUCTIVE_TASK_BLOCKED, [t.task_id], "CRITICAL", f"Destructive task blocked: {t.command}", True, {}))
    return conflicts

def conflicts_to_text(conflicts: List[TaskConflict], limit: int = 50) -> str:
    lines = [f"Task Conflicts (Found: {len(conflicts)})", "=" * 40]
    for c in conflicts[:limit]:
        lines.extend([f"[{c.severity}] {c.conflict_type.value}: {c.message}", f"Tasks: {', '.join(c.task_ids)}", "-" * 20])
    return "\n".join(lines)
