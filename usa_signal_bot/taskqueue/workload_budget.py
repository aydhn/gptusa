from typing import List, Optional, Dict, Any
from usa_signal_bot.taskqueue.task_models import LocalTask, WorkloadBudget, WorkloadBudgetEvaluation, create_workload_budget_id, create_workload_evaluation_id
from usa_signal_bot.core.enums import WorkloadBudgetStatus
from datetime import datetime, timezone

def default_workload_budget() -> WorkloadBudget:
    return WorkloadBudget(budget_id=create_workload_budget_id("average_local_pc"), name="Average Local PC", max_cpu_pct=85.0, max_gpu_pct=70.0, max_ram_mb=8192.0, max_disk_mb=2048.0, max_network_mb_per_run=1024.0, max_duration_seconds=7200.0, max_parallel_tasks=1)

def conservative_workload_budget() -> WorkloadBudget:
    budget = default_workload_budget()
    budget.name = "Conservative Profile"
    budget.max_cpu_pct = 50.0
    budget.max_ram_mb = 4096.0
    budget.max_disk_mb = 1024.0
    return budget

def evaluate_workload_budget(tasks: List[LocalTask], budget: Optional[WorkloadBudget] = None) -> WorkloadBudgetEvaluation:
    b = budget or default_workload_budget()
    cpu = sum(t.estimated_cpu_pct or 0.0 for t in tasks)
    gpu = sum(t.estimated_gpu_pct or 0.0 for t in tasks)
    ram = sum(t.estimated_ram_mb or 0.0 for t in tasks)
    disk = sum(t.estimated_disk_mb or 0.0 for t in tasks)
    network = sum(t.estimated_network_mb or 0.0 for t in tasks)
    duration = sum(t.estimated_duration_seconds or 0.0 for t in tasks)
    warnings, errors = [], []
    if cpu > b.max_cpu_pct: errors.append(f"Estimated CPU ({cpu}%) exceeds budget ({b.max_cpu_pct}%)")
    if gpu > b.max_gpu_pct: errors.append(f"Estimated GPU ({gpu}%) exceeds budget ({b.max_gpu_pct}%)")
    if ram > b.max_ram_mb: errors.append(f"Estimated RAM ({ram}MB) exceeds budget ({b.max_ram_mb}MB)")
    if disk > b.max_disk_mb: errors.append(f"Estimated Disk IO ({disk}MB) exceeds budget ({b.max_disk_mb}MB)")
    if network > b.max_network_mb_per_run: errors.append(f"Estimated Network ({network}MB) exceeds budget ({b.max_network_mb_per_run}MB)")
    if duration > b.max_duration_seconds: warnings.append(f"Estimated duration ({duration}s) exceeds budget target ({b.max_duration_seconds}s)")
    status = WorkloadBudgetStatus.EXCEEDED if errors else (WorkloadBudgetStatus.WARNING if warnings else WorkloadBudgetStatus.WITHIN_BUDGET)
    return WorkloadBudgetEvaluation(evaluation_id=create_workload_evaluation_id(), created_at_utc=datetime.now(timezone.utc).isoformat(), status=status, budget=b, tasks=tasks, total_estimated_cpu_pct=cpu, total_estimated_gpu_pct=gpu, total_estimated_ram_mb=ram, total_estimated_disk_mb=disk, total_estimated_network_mb=network, total_estimated_duration_seconds=duration, warnings=warnings, errors=errors)

def classify_budget_status(evaluation: WorkloadBudgetEvaluation) -> WorkloadBudgetStatus:
    return evaluation.status

def workload_budget_to_text(budget: WorkloadBudget) -> str:
    return "\n".join([f"Workload Budget Profile: {budget.name}", f"CPU: {budget.max_cpu_pct}% | GPU: {budget.max_gpu_pct}%", f"RAM: {budget.max_ram_mb}MB | Disk: {budget.max_disk_mb}MB", f"Network: {budget.max_network_mb_per_run}MB | Duration: {budget.max_duration_seconds}s", f"Max Parallel: {budget.max_parallel_tasks}"])

def workload_budget_evaluation_to_text(evaluation: WorkloadBudgetEvaluation) -> str:
    lines = ["Workload Budget Evaluation", f"Status: {evaluation.status.value}", "-" * 30, f"CPU: {evaluation.total_estimated_cpu_pct}% / {evaluation.budget.max_cpu_pct}%", f"RAM: {evaluation.total_estimated_ram_mb}MB / {evaluation.budget.max_ram_mb}MB", f"Disk: {evaluation.total_estimated_disk_mb}MB / {evaluation.budget.max_disk_mb}MB", f"Network: {evaluation.total_estimated_network_mb}MB / {evaluation.budget.max_network_mb_per_run}MB", f"Duration: {evaluation.total_estimated_duration_seconds}s / {evaluation.budget.max_duration_seconds}s"]
    if evaluation.errors: lines.extend(["Errors:"] + [f"- {e}" for e in evaluation.errors])
    if evaluation.warnings: lines.extend(["Warnings:"] + [f"- {w}" for w in evaluation.warnings])
    return "\n".join(lines)
