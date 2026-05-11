from typing import Optional, List
from pathlib import Path
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskQueuePlan, TaskQueueRunResult, create_task_queue_run_id
from usa_signal_bot.core.enums import LocalTaskStatus, TaskQueueStatus
from datetime import datetime, timezone

class TaskQueueDryRunExecutor:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None):
        self.data_root = data_root

    def execute_plan(self, plan: TaskQueuePlan) -> TaskQueueRunResult:
        if any(c.blocking for c in plan.conflicts):
            return TaskQueueRunResult(create_task_queue_run_id(), datetime.now(timezone.utc).isoformat(), TaskQueueStatus.BLOCKED, plan, [], plan.tasks, [], [], {}, ["Plan execution blocked due to plan-level conflicts."], [])
        executed, skipped, blocked, failed = [], [], [], []
        for task in plan.tasks:
            t = self.execute_task(task)
            if t.status == LocalTaskStatus.COMPLETED: executed.append(t)
            elif t.status == LocalTaskStatus.BLOCKED: blocked.append(t)
            elif t.status == LocalTaskStatus.SKIPPED: skipped.append(t)
            else: failed.append(t)
        status = TaskQueueStatus.WARNING if failed or blocked else TaskQueueStatus.DRY_RUN_COMPLETED
        return TaskQueueRunResult(create_task_queue_run_id(), datetime.now(timezone.utc).isoformat(), status, plan, executed, skipped, blocked, failed, {}, [], [])

    def execute_task(self, task: LocalTask) -> LocalTask:
        if task.status == LocalTaskStatus.BLOCKED: return task
        if task.command and any(d in task.command for d in ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]):
            return self.block_task(task, "Destructive command detected during execution")
        task.status = LocalTaskStatus.COMPLETED
        task.metadata["executed_as"] = "dry_run"
        return task

    def block_task(self, task: LocalTask, reason: str) -> LocalTask:
        task.status = LocalTaskStatus.BLOCKED
        task.metadata["blocked_reason"] = reason
        return task

    def write_result(self, result: TaskQueueRunResult) -> List[Path]:
        from usa_signal_bot.taskqueue.taskqueue_store import write_task_queue_run_result_json
        return [write_task_queue_run_result_json(self.data_root / "taskqueue" / "runs" / f"{result.run_id}.json", result)]
