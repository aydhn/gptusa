from typing import Dict, Any
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskPriorityScore, ResourceEstimate, WorkloadBudget, WorkloadBudgetEvaluation, TaskConflict, TaskQueuePlan, TaskQueueRunResult
from pathlib import Path

def local_task_to_text(task: LocalTask) -> str:
    from usa_signal_bot.taskqueue.task_catalog import local_tasks_to_text
    return local_tasks_to_text([task])

def task_priority_score_to_text(score: TaskPriorityScore) -> str:
    from usa_signal_bot.taskqueue.priority_scoring import priority_scores_to_text
    return priority_scores_to_text([score])

def resource_estimate_to_text(estimate: ResourceEstimate) -> str:
    from usa_signal_bot.taskqueue.resource_estimator import resource_estimates_to_text
    return resource_estimates_to_text([estimate])

def workload_budget_report_to_text(budget: WorkloadBudget) -> str:
    from usa_signal_bot.taskqueue.workload_budget import workload_budget_to_text
    return workload_budget_to_text(budget)

def workload_budget_evaluation_report_to_text(evaluation: WorkloadBudgetEvaluation) -> str:
    from usa_signal_bot.taskqueue.workload_budget import workload_budget_evaluation_to_text
    return workload_budget_evaluation_to_text(evaluation)

def task_conflict_to_text(conflict: TaskConflict) -> str:
    from usa_signal_bot.taskqueue.conflict_detector import conflicts_to_text
    return conflicts_to_text([conflict])

def task_queue_plan_to_text(plan: TaskQueuePlan, limit: int = 50) -> str:
    lines = ["Task Queue Plan", "=" * 40, f"Plan ID: {plan.plan_id}", f"Status: {plan.status.value}", f"Dry Run: {plan.dry_run}", f"Tasks: {len(plan.tasks)}"]
    if plan.budget_evaluation: lines.append(f"\nBudget Status: {plan.budget_evaluation.status.value}")
    if plan.conflicts:
        lines.append(f"\nConflicts Found: {len(plan.conflicts)}")
        for c in plan.conflicts[:5]: lines.append(f"- [{c.severity}] {c.message}")
    if plan.errors:
        lines.append("\nErrors:")
        for e in plan.errors: lines.append(f"- {e}")
    return "\n".join(lines)

def task_queue_run_result_to_text(result: TaskQueueRunResult, limit: int = 50) -> str:
    lines = ["Task Queue Run Result", "=" * 40, f"Run ID: {result.run_id}", f"Status: {result.status.value}", f"Executed: {len(result.executed_tasks)}", f"Skipped: {len(result.skipped_tasks)}", f"Blocked: {len(result.blocked_tasks)}", f"Failed: {len(result.failed_tasks)}"]
    if result.errors:
        lines.append("\nErrors:")
        for e in result.errors: lines.append(f"- {e}")
    return "\n".join(lines)

def taskqueue_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return "\n".join(["Task Queue Store Summary", "=" * 40, f"Total Plans: {summary['plans_count']}", f"Total Runs: {summary['runs_count']}", f"Latest Plan: {summary['latest_plan']}", f"Latest Run: {summary['latest_run']}"])

def taskqueue_limitations_text() -> str:
    return "\nTASK QUEUE SIMULATION LIMITATIONS\n=================================\n1. This is a local simulation only.\n2. There is no real background worker, daemon, or cron service.\n3. No real broker API calls are made.\n4. No live or demo orders are executed.\n5. Resource estimates are purely heuristic, not measured via psutil or GPU sensors.\n6. A 'PASS' status does NOT constitute live execution approval or investment advice.\n"

def write_taskqueue_report_json(path: Path, result: TaskQueueRunResult, validation_report: Any = None) -> Path:
    from usa_signal_bot.taskqueue.taskqueue_store import write_task_queue_run_result_json
    return write_task_queue_run_result_json(path, result)
