from typing import List, Optional
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskQueuePlan
from usa_signal_bot.scheduler.scheduler_models import SchedulerJob, SchedulerPlan, SchedulerJobType, SchedulerJobStatus, SchedulerPlanStatus
from usa_signal_bot.scheduler.concurrency_guard import ConcurrencyDecisionResult, ConcurrencyGuard
from usa_signal_bot.core.enums import RunLockScope, LocalTaskType, LocalTaskStatus

def scheduler_job_from_local_task(task: LocalTask) -> SchedulerJob:
    job_type = SchedulerJobType.CUSTOM
    try: job_type = SchedulerJobType(task.task_type.value)
    except ValueError: pass
    return SchedulerJob(f"job_mapped_{task.task_id}", job_type, task.name, task.command or "echo NO_COMMAND", task.lock_scope, True, SchedulerJobStatus.BLOCKED if task.status == LocalTaskStatus.BLOCKED else SchedulerJobStatus.PLANNED, task.dry_run, [], {"source_task_id": task.task_id, "priority": task.priority.value})

def local_task_from_scheduler_job(job: SchedulerJob) -> LocalTask:
    from usa_signal_bot.taskqueue.task_catalog import task_for_type
    from usa_signal_bot.core.enums import TaskPriority
    try: return task_for_type(LocalTaskType(job.job_type.value), dry_run=job.dry_run)
    except Exception:
        task = LocalTask(job.job_id, LocalTaskType.CUSTOM, job.name, TaskPriority.NORMAL, LocalTaskStatus.BLOCKED if job.status == SchedulerJobStatus.BLOCKED else LocalTaskStatus.CREATED, job.command, RunLockScope(job.scope), 0, 0, 0, 0, 0, 0, job.dry_run)
        return task

def scheduler_plan_from_task_queue_plan(plan: TaskQueuePlan) -> SchedulerPlan:
    return SchedulerPlan(f"splan_{plan.plan_id}", plan.created_at_utc, SchedulerPlanStatus.VALIDATED, plan.dry_run, [scheduler_job_from_local_task(t) for t in plan.tasks], plan.warnings, plan.errors)

def task_queue_plan_from_scheduler_plan(plan: SchedulerPlan) -> TaskQueuePlan:
    from usa_signal_bot.taskqueue.task_models import create_task_queue_plan_id
    from usa_signal_bot.core.enums import TaskQueueStatus
    return TaskQueuePlan(create_task_queue_plan_id(), plan.created_at_utc, TaskQueueStatus.PLANNED, plan.dry_run, [local_task_from_scheduler_job(j) for j in plan.jobs], [], None, [], [], plan.warnings, plan.errors)
