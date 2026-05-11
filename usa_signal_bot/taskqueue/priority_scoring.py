from typing import List, Dict, Any, Optional
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskPriorityScore, WorkloadBudget, create_priority_score_id
from usa_signal_bot.core.enums import TaskPriority

def priority_base_score(priority: TaskPriority) -> float:
    return {TaskPriority.CRITICAL: 100.0, TaskPriority.URGENT: 80.0, TaskPriority.HIGH: 60.0, TaskPriority.NORMAL: 40.0, TaskPriority.LOW: 20.0}.get(priority, 40.0)

def calculate_urgency_score(task: LocalTask, context: Optional[Dict[str, Any]] = None) -> float:
    return 30.0 if context and context.get("incident_active", False) and task.task_type.value == "INCIDENT_REVIEW" else 0.0

def calculate_safety_score(task: LocalTask, context: Optional[Dict[str, Any]] = None) -> float:
    if task.task_type.value in ["CONFIG_VALIDATION", "HEALTH_CHECK"]: return 25.0
    if task.task_type.value == "REGRESSION_RUN": return 10.0
    if task.task_type.value == "CLEANUP_DRY_RUN" and context and context.get("quota_warning", False): return 15.0
    return 0.0

def calculate_freshness_score(task: LocalTask, context: Optional[Dict[str, Any]] = None) -> float:
    return 0.0

def calculate_workload_penalty(task: LocalTask, budget: Optional[WorkloadBudget] = None) -> float:
    penalty = 0.0
    if task.estimated_cpu_pct and task.estimated_cpu_pct > 50.0: penalty += 10.0
    if task.estimated_ram_mb and task.estimated_ram_mb > 4096.0: penalty += 10.0
    if task.estimated_duration_seconds and task.estimated_duration_seconds > 1800.0: penalty += 15.0
    return penalty

def calculate_task_priority_score(task: LocalTask, context: Optional[Dict[str, Any]] = None, budget: Optional[WorkloadBudget] = None) -> TaskPriorityScore:
    base = priority_base_score(task.priority)
    urgency = calculate_urgency_score(task, context)
    safety = calculate_safety_score(task, context)
    freshness = calculate_freshness_score(task, context)
    penalty = calculate_workload_penalty(task, budget) if (context and context.get("workload_penalty_enabled", True)) else 0.0
    return TaskPriorityScore(task_id=task.task_id, base_priority=task.priority, score=max(0.0, base + urgency + safety + freshness - penalty), urgency_score=urgency, safety_score=safety, freshness_score=freshness, workload_penalty=penalty, reason=f"Base: {base}, Urgency: {urgency}, Safety: {safety}, Freshness: {freshness}, Penalty: {penalty}", metadata={})

def score_tasks(tasks: List[LocalTask], context: Optional[Dict[str, Any]] = None, budget: Optional[WorkloadBudget] = None) -> List[TaskPriorityScore]:
    return [calculate_task_priority_score(t, context, budget) for t in tasks]

def sort_tasks_by_priority(tasks: List[LocalTask], scores: List[TaskPriorityScore]) -> List[LocalTask]:
    score_map = {s.task_id: s.score for s in scores}
    return sorted(tasks, key=lambda t: (-score_map.get(t.task_id, 0.0), t.name))

def priority_scores_to_text(scores: List[TaskPriorityScore], limit: int = 50) -> str:
    lines = ["Task Priority Scoring", "=" * 40]
    for s in sorted(scores, key=lambda x: x.score, reverse=True)[:limit]:
        lines.extend([f"Task ID: {s.task_id}", f"Score: {s.score:.1f} (Base: {s.base_priority.value})", f"Details: {s.reason}", "-" * 20])
    return "\n".join(lines)
