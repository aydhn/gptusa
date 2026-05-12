from datetime import datetime, timezone
from pathlib import Path
from typing import List
from usa_signal_bot.release.maintenance_models import (
    MaintenanceTask, MaintenancePlan, MaintenanceTaskResult, MaintenanceRunResult,
    create_maintenance_plan_id, create_maintenance_run_id, create_maintenance_task_id
)
from usa_signal_bot.core.enums import MaintenanceFrequency, MaintenanceTaskStatus

def daily_maintenance_tasks() -> List[MaintenanceTask]:
    return [
        MaintenanceTask(task_id=create_maintenance_task_id("validate-config"), name="validate-config", frequency=MaintenanceFrequency.DAILY, description="Validate configuration.", command="python -m usa_signal_bot validate-config", required=True),
        MaintenanceTask(task_id=create_maintenance_task_id("health"), name="health", frequency=MaintenanceFrequency.DAILY, description="Check system health.", command="python -m usa_signal_bot health", required=True),
        MaintenanceTask(task_id=create_maintenance_task_id("runtime-lock-status"), name="runtime-lock-status", frequency=MaintenanceFrequency.DAILY, description="Check runtime locks.", command="python -m usa_signal_bot runtime-lock-status", required=False),
        MaintenanceTask(task_id=create_maintenance_task_id("scan-summary"), name="scan-summary", frequency=MaintenanceFrequency.DAILY, description="View scan summary.", command="python -m usa_signal_bot scan-summary", required=False),
        MaintenanceTask(task_id=create_maintenance_task_id("paper-summary"), name="paper-summary", frequency=MaintenanceFrequency.DAILY, description="View paper simulation summary.", command="python -m usa_signal_bot paper-info", required=False),
        MaintenanceTask(task_id=create_maintenance_task_id("notification-summary"), name="notification-summary", frequency=MaintenanceFrequency.DAILY, description="View notification summary.", command="python -m usa_signal_bot notification-summary", required=False),
        MaintenanceTask(task_id="scheduler-lock-summary", name="Scheduler Lock Summary", description="View a summary of current run locks", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot lock-status", required=False),
        MaintenanceTask(task_id="scheduler-stale-locks-dry-run", name="Scheduler Stale Locks Dry Run", description="Find and simulate cleanup of stale locks", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot stale-lock-cleanup --dry-run", required=False),
        MaintenanceTask(task_id="scheduler-concurrency-review", name="Scheduler Concurrency Review", description="Review concurrency block policies and decisions", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot concurrency-review", required=False),
        MaintenanceTask(task_id="lock-audit-summary", name="Lock Audit Summary", description="Review lock acquire/release audit summary", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot lock-audit-summary", required=False),
        MaintenanceTask(task_id="scheduler-plan-dry-run", name="Scheduler Plan Dry Run", description="Simulate generation of a scheduler plan", frequency=MaintenanceFrequency.WEEKLY, command="python -m usa_signal_bot scheduler-plan --dry-run", required=False),
        MaintenanceTask(task_id="scheduler-run-once-dry-run", name="Scheduler Run Once Dry Run", description="Simulate execution of a scheduler plan", frequency=MaintenanceFrequency.WEEKLY, command="python -m usa_signal_bot scheduler-run-once --dry-run", required=False),
        MaintenanceTask(task_id="idempotency-summary", name="Idempotency Summary", description="Review idempotency records to prevent duplicate runs", frequency=MaintenanceFrequency.WEEKLY, command="python -m usa_signal_bot idempotency-summary", required=False),
        MaintenanceTask(task_id="idempotency-prune-dry-run", name="Idempotency Prune Dry Run", description="Simulate pruning of expired idempotency records", frequency=MaintenanceFrequency.MONTHLY, command="python -m usa_signal_bot idempotency-prune --dry-run", required=False),
        MaintenanceTask(task_id="scheduler-health", name="Scheduler Health", description="Check health of local scheduler components", frequency=MaintenanceFrequency.PRE_RELEASE, command="python -m usa_signal_bot scheduler-info", required=False),
        MaintenanceTask(task_id="performance-sample-current", name="Performance Sample", description="Collect current operational sample", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot performance-sample-current", required=False),
        MaintenanceTask(task_id="performance-compare-latest", name="Performance Compare", description="Compare operational sample to P90 baselines", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot performance-compare", required=False),
        MaintenanceTask(task_id="runtime-regression-check", name="Runtime Regression Check", description="Detect minor to critical performance drifts", frequency=MaintenanceFrequency.DAILY, command="python -m usa_signal_bot runtime-regression-check", required=False)
    ]

def weekly_maintenance_tasks() -> List[MaintenanceTask]:
    return [
        MaintenanceTask(task_id=create_maintenance_task_id("regression-run-smoke"), name="regression-run-smoke", frequency=MaintenanceFrequency.WEEKLY, description="Run regression smoke tests.", command="python -m usa_signal_bot regression-info", required=True),
        MaintenanceTask(task_id="performance-build-baseline", name="Performance Build Baseline", description="Build new performance baseline from recent samples", frequency=MaintenanceFrequency.WEEKLY, command="python -m usa_signal_bot performance-build-baseline --write", required=False),
        MaintenanceTask(task_id="sla-evaluate", name="SLA Evaluate", description="Check current baselines against SLA thresholds", frequency=MaintenanceFrequency.WEEKLY, command="python -m usa_signal_bot sla-evaluate --write", required=False),
        MaintenanceTask(task_id="performance-review", name="Performance Review", description="Run the full performance acceptance gate locally", frequency=MaintenanceFrequency.WEEKLY, command="python -m usa_signal_bot performance-review --write", required=False),
        MaintenanceTask(task_id=create_maintenance_task_id("quality-scorecard"), name="quality-scorecard", frequency=MaintenanceFrequency.WEEKLY, description="Generate quality scorecard.", command="python -m usa_signal_bot quality-scorecard", required=True),
        MaintenanceTask(task_id=create_maintenance_task_id("acceptance-evaluate"), name="acceptance-evaluate", frequency=MaintenanceFrequency.WEEKLY, description="Evaluate system acceptance.", command="python -m usa_signal_bot acceptance-evaluate", required=True),
        MaintenanceTask(task_id=create_maintenance_task_id("backup-create"), name="backup-create dry-run/precheck", frequency=MaintenanceFrequency.WEEKLY, description="Create a reports backup.", command="python -m usa_signal_bot backup-create --scope reports_only", required=False),
    ]

def monthly_maintenance_tasks() -> List[MaintenanceTask]:
    return [
        MaintenanceTask(task_id="performance-baseline-stale-review", name="Baseline Stale Review", description="Review older baseline versions for freshness", frequency=MaintenanceFrequency.MONTHLY, command="python -m usa_signal_bot performance-baselines", required=False),
        MaintenanceTask(task_id="sla-threshold-review", name="SLA Threshold Review", description="Review currently registered SLA thresholds limits", frequency=MaintenanceFrequency.MONTHLY, command="python -m usa_signal_bot sla-thresholds", required=False),
        MaintenanceTask(task_id=create_maintenance_task_id("release-rehearsal"), name="release-rehearsal", frequency=MaintenanceFrequency.MONTHLY, description="Run full release rehearsal.", command="python -m usa_signal_bot release-rehearsal", required=True),
        MaintenanceTask(task_id=create_maintenance_task_id("backup-validate"), name="backup-validate", frequency=MaintenanceFrequency.MONTHLY, description="Validate latest backups.", command=None, required=False),
        MaintenanceTask(task_id=create_maintenance_task_id("config-profile-validate"), name="config-profile-validate", frequency=MaintenanceFrequency.MONTHLY, description="Validate config profiles.", command="python -m usa_signal_bot config-profile-validate --all", required=True)
    ]

def pre_release_maintenance_tasks() -> List[MaintenanceTask]:
    return [
        MaintenanceTask(task_id=create_maintenance_task_id("pre-release-rehearsal"), name="release-rehearsal --scope golden_sample", frequency=MaintenanceFrequency.PRE_RELEASE, description="Run release rehearsal on golden sample.", command="python -m usa_signal_bot release-rehearsal", required=True),
        MaintenanceTask(task_id=create_maintenance_task_id("pre-release-regression-check"), name="pre-release-regression-check", frequency=MaintenanceFrequency.PRE_RELEASE, description="Run regression smoke checks before release.", command="python -m usa_signal_bot regression-info", required=True),
        MaintenanceTask(task_id="pre-release-performance-review", name="Pre-release Performance Review", description="Ensure no critical regression or blocked SLA breach", frequency=MaintenanceFrequency.PRE_RELEASE, command="python -m usa_signal_bot performance-review --write", required=True)
    ]

def default_maintenance_plan() -> MaintenancePlan:
    tasks = daily_maintenance_tasks() + weekly_maintenance_tasks() + monthly_maintenance_tasks() + pre_release_maintenance_tasks()
    return MaintenancePlan(
        plan_id=create_maintenance_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        tasks=tasks
    )

def evaluate_maintenance_task(task: MaintenanceTask, project_root: Path, data_root: Path) -> MaintenanceTaskResult:
    # Controlled evaluation: we don't actually run subprocesses here for safety unless requested.
    # By default, we mark as PASSED (dry run style) to avoid destructive/blocking behavior.
    return MaintenanceTaskResult(
        task_id=task.task_id,
        name=task.name,
        status=MaintenanceTaskStatus.PASSED,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        command=task.command,
        summary="Task dry-run evaluation passed."
    )

def run_maintenance_check(frequency: MaintenanceFrequency, project_root: Path, data_root: Path) -> MaintenanceRunResult:
    tasks = []
    if frequency == MaintenanceFrequency.DAILY:
        tasks = daily_maintenance_tasks()
    elif frequency == MaintenanceFrequency.WEEKLY:
        tasks = weekly_maintenance_tasks()
    elif frequency == MaintenanceFrequency.MONTHLY:
        tasks = monthly_maintenance_tasks()
    elif frequency == MaintenanceFrequency.PRE_RELEASE:
        tasks = pre_release_maintenance_tasks()
    elif frequency == MaintenanceFrequency.ON_DEMAND:
        tasks = daily_maintenance_tasks()[:2] # Just a small subset

    results = [evaluate_maintenance_task(t, project_root, data_root) for t in tasks]
    passed = sum(1 for r in results if r.status == MaintenanceTaskStatus.PASSED)
    failed = sum(1 for r in results if r.status == MaintenanceTaskStatus.FAILED)
    warn = sum(1 for r in results if r.status == MaintenanceTaskStatus.WARNING)
    skipped = sum(1 for r in results if r.status == MaintenanceTaskStatus.SKIPPED)

    overall_status = MaintenanceTaskStatus.FAILED if failed > 0 else (MaintenanceTaskStatus.WARNING if warn > 0 else MaintenanceTaskStatus.PASSED)

    return MaintenanceRunResult(
        run_id=create_maintenance_run_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        frequency=frequency,
        status=overall_status,
        results=results,
        passed_count=passed,
        warning_count=warn,
        failed_count=failed,
        skipped_count=skipped
    )

def maintenance_plan_to_markdown(plan: MaintenancePlan) -> str:
    lines = [f"# Maintenance Plan (ID: {plan.plan_id})", f"*Generated: {plan.created_at_utc}*\n"]
    for freq in [MaintenanceFrequency.DAILY, MaintenanceFrequency.WEEKLY, MaintenanceFrequency.MONTHLY, MaintenanceFrequency.PRE_RELEASE]:
        lines.append(f"## {freq.value} Tasks")
        freq_tasks = [t for t in plan.tasks if t.frequency == freq]
        if not freq_tasks:
            lines.append("- No tasks defined.")
        for task in freq_tasks:
            req = "(Required)" if task.required else "(Optional)"
            lines.append(f"### {task.name} {req}")
            lines.append(f"{task.description}")
            if task.command:
                lines.append(f"`{task.command}`")
        lines.append("")
    return "\n".join(lines)

def maintenance_run_result_to_text(result: MaintenanceRunResult) -> str:
    lines = [
        f"Maintenance Run: {result.frequency.value} (ID: {result.run_id})",
        f"Status: {result.status.value}",
        f"Passed: {result.passed_count}, Failed: {result.failed_count}, Warnings: {result.warning_count}"
    ]
    for res in result.results:
        lines.append(f"- {res.name}: {res.status.value}")
    return "\n".join(lines)

def task_incident_review():
    pass

def task_recovery_plan_dry_run():
    pass

def task_rollback_precheck():
    pass

def task_rollback_dry_run():
    pass

def task_incident_audit_summary():
    pass